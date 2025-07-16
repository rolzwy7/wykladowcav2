# flake8: noqa:E501
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.timezone import now, timedelta

from core.models import (
    CrmNote,
    MailingCampaign,
    MailingTitleTest,
    Webinar,
    WebinarApplication,
    WebinarCategory,
    WebinarParticipant,
    WebinarQueue,
)
from core.models.enums import ApplicationStatus
from core.services import CrmWebinarService


def crm_upcoming_webinars(request):
    """CRM upcoming webinars"""

    webinars = Webinar.manager.get_init_or_confirmed_or_draft_webinars()

    param_any = False

    # Show only drafts
    param_show_only_drafts = request.GET.get("show_only_drafts")
    if param_show_only_drafts:
        param_any = True
        webinars = Webinar.manager.get_draft_webinars()
    else:
        webinars = Webinar.manager.get_init_or_confirmed_or_draft_webinars()

    # Main categories
    main_categories = WebinarCategory.manager.get_main_categories()
    param_main_category = request.GET.get("param_main_category")
    selected_main_category = None
    if param_main_category and param_main_category != "all":
        webinars = webinars.filter(categories__slug__in=[param_main_category])
        param_any = True
        selected_main_category = WebinarCategory.manager.get(slug=param_main_category)

    # Show counters
    param_show_counters = request.GET.get("show_counters")
    if param_show_counters:
        param_any = True

    # Hide old webinars
    param_hide_old = request.GET.get("hide_old")
    if param_hide_old:
        webinars = webinars.filter(date__gt=now())
        param_any = True

    # Hide fake param
    param_hide_fake = request.GET.get("hide_fake")
    if param_hide_fake:
        webinars = webinars.filter(is_fake=False)
        param_any = True

    # Search param
    param_search = request.GET.get("search")
    if param_search:
        webinars = webinars.filter(
            Q(title_original__icontains=param_search)
            | Q(title__icontains=param_search)
            | Q(grouping_token__icontains=param_search)
            | Q(lecturer__fullname__icontains=param_search)
        )
        param_any = True

    sent_today_paid_applications = WebinarApplication.manager.filter(
        status=ApplicationStatus.SENT, created_at__date=timezone.now().date()
    )

    if cache.get("CACHE_PERFORM_SENTINEL_total_netto") is not None:
        today_total_netto = cache.get("CACHE_PERFORM_today_total_netto")
        sent_today_paid_applications_with_netto = cache.get(
            "CACHE_PERFORM_sent_today_paid_applications_with_netto"
        )
    else:
        # Total netto value of todays webinars
        today_total_netto = 0
        sent_today_paid_applications_with_netto = []
        for application in sent_today_paid_applications:
            count_participants = (
                WebinarParticipant.manager.get_valid_participants_for_application(
                    application
                ).count()
            )
            today_total_netto += application.price_netto * count_participants

            try:
                campaign = MailingCampaign.manager.get(id=int(application.campaign_id))
            except MailingCampaign.DoesNotExist:  # pylint: disable=no-member
                campaign = None
            except (TypeError, ValueError):
                campaign = None

            sent_today_paid_applications_with_netto.append(
                (
                    application,
                    count_participants,
                    application.price_netto * count_participants,
                    campaign,
                )
            )

            cache.set("CACHE_PERFORM_SENTINEL_total_netto", True, timeout=300)
            cache.set("CACHE_PERFORM_today_total_netto", today_total_netto, timeout=600)
            cache.set(
                "CACHE_PERFORM_sent_today_paid_applications_with_netto",
                sent_today_paid_applications_with_netto,
                timeout=600,
            )

    # Webinars added today
    webinars_added_today = Webinar.manager.filter(
        created_at__date=timezone.now().date()
    )

    # Webinar Queue
    webinar_queue_map = {}
    for webinar_queue in WebinarQueue.manager.all():
        if webinar_queue.aggregate.grouping_token not in webinar_queue_map:
            webinar_queue_map[webinar_queue.aggregate.grouping_token] = [
                webinar_queue.aggregate.title,
                0,
                0,
            ]
        if webinar_queue.sent_notification:
            webinar_queue_map[webinar_queue.aggregate.grouping_token][1] += 1
        else:
            webinar_queue_map[webinar_queue.aggregate.grouping_token][2] += 1

    if cache.get("CACHE_PERFORM_sending_campaigns_with_test_subjects") is not None:
        sending_campaigns_with_test_subjects = cache.get(
            "CACHE_PERFORM_sending_campaigns_with_test_subjects"
        )
    else:
        # Active mailing campaigns
        sending_campaigns = MailingCampaign.manager.filter(
            Q(created_at__gte=now() - timedelta(days=1, hours=8)) & ~Q(stat_sent=0)
        )
        # sending_campaigns = MailingCampaign.manager.filter(
        #     status=MailingCampaignStatus.SENDING
        # )
        sending_campaigns_with_test_subjects = [
            (
                _,
                [
                    mt
                    for mt in MailingTitleTest.objects.filter(  # pylint: disable=no-member
                        campaign_id=_.id
                    ).order_by(
                        "title"
                    )
                ],
            )
            for _ in sending_campaigns
        ]
        cache.set(
            "CACHE_PERFORM_sending_campaigns_with_test_subjects",
            sending_campaigns_with_test_subjects,
            timeout=600,
        )

    return TemplateResponse(
        request,
        "core/pages/crm/webinar/CrmUpcomingWebinars.html",
        {
            "webinars_added_today": webinars_added_today,
            "webinars_added_today_count": webinars_added_today.count(),
            "webinar_queue_map": webinar_queue_map,
            "webinar_queue_map_count": len(webinar_queue_map),
            "sending_campaigns_with_test_subjects": sending_campaigns_with_test_subjects,
            "sending_campaigns_with_test_subjects_count": len(
                sending_campaigns_with_test_subjects
            ),
            "main_categories": main_categories,
            "selected_main_category": selected_main_category,
            "crm_notes": CrmNote.manager.get_notes(),
            "upcoming_webinars_count": webinars.count(),
            "sent_today_paid_applications": sent_today_paid_applications,
            "sent_today_paid_applications_with_netto": sent_today_paid_applications_with_netto,
            "sent_today_paid_applications_count": sent_today_paid_applications.count(),
            "today_total_netto": f"{today_total_netto:,} zł",
            # "sent_today_paid_applications_total_netto": f"{sent_today_paid_applications_total_netto:,} zł",
            "mailing_processes_num": settings.MAILING_NUM_OF_PROCESSES,
            "param_any": param_any,
            "param_hide_old": param_hide_old,
            "param_search": param_search or "",
            "param_hide_fake": param_hide_fake,
            "param_show_counters": param_show_counters,
            "param_show_only_drafts": param_show_only_drafts,
            "param_main_category": param_main_category,
            # "webinars_ctxs": [
            #     CrmWebinarService(webinar).get_context() for webinar in webinars
            # ],
            "webinars_ctxs_upcoming_webinar_row": [
                CrmWebinarService(webinar).get_upcoming_webinar_row_context()
                for webinar in webinars
            ],
        },
    )
