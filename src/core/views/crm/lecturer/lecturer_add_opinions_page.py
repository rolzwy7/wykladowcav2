import hashlib
from random import randint

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.timezone import now, timedelta

from core.consts import POST
from core.forms.crm import CrmLecturerAddOpinionsForm
from core.models import Lecturer, LecturerOpinion
from core.models.enums import LecturerOpinionRating


def try_to_add_opinion(lecturer: Lecturer, opinion_raw: str):
    """Try to add opinion for lecturer"""

    # Normalize raw opinion
    opinion_normalized = opinion_raw.strip()
    if not opinion_normalized:
        return

    # Split by special character/sequence
    try:
        (
            rating,
            fullname,
            opinion_text,
            company_name,
            job_title,
        ) = opinion_normalized.split("#")
    except ValueError:
        return
    else:
        rating = rating.strip()
        fullname = fullname.strip()
        opinion_text = opinion_text.strip()
        company_name = company_name.strip()
        job_title = job_title.strip()

    # Make opinion hash
    opinion_hash = hashlib.sha256(opinion_text.encode()).hexdigest()
    already_exists = LecturerOpinion.manager.filter(
        opinion_hash=opinion_hash
    ).exists()

    # Give up if already exists
    if already_exists:
        return

    # Set default rating if incorrect
    possible_stars = [
        LecturerOpinionRating.STARS_5,
        LecturerOpinionRating.STARS_4,
        LecturerOpinionRating.STARS_3,
        LecturerOpinionRating.STARS_2,
        LecturerOpinionRating.STARS_1,
    ]
    if rating not in possible_stars:
        rating = LecturerOpinionRating.STARS_5

    # Create and save new opinion about lecturer
    opinion = LecturerOpinion(
        visible_on_page=True,
        lecturer=lecturer,
        fullname=fullname,
        company_name=company_name,
        job_title=job_title,
        opinion_text=opinion_text,
        rating=rating,
        opinion_hash=opinion_hash,
    )
    opinion.created_at = now() - timedelta(hours=30 * randint(0, 24))
    opinion.save()


def lecturer_add_opinions_page(request, pk: int):
    """Lecturer add opinions page"""
    template_name = "core/pages/crm/lecturer/LecturerAddOpinionsPage.html"
    lecturer = get_object_or_404(Lecturer, pk=pk)

    if request.method == POST:
        form = CrmLecturerAddOpinionsForm(request.POST)
        if form.is_valid():
            opinions = request.POST["opinions"]
            for opinion in opinions.split("\r\n"):
                try_to_add_opinion(lecturer, opinion)
            return redirect(
                reverse(
                    "core:lecturer_add_opinions_page",
                    kwargs={"pk": lecturer.pk},
                )
            )

    else:
        form = CrmLecturerAddOpinionsForm()

    return TemplateResponse(request, template_name, {"lecturer": lecturer})
