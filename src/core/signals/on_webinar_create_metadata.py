"""On Webinar create metadata"""

# flake8: noqa=E501

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.libs.webinar_aggregate import (
    aggregate_add_category,
    aggregate_add_webinar,
    aggregate_update_conflicts,
    get_or_create_aggregate,
)
from core.models import Webinar, WebinarMetadata


@receiver(post_save, sender=Webinar, dispatch_uid="768af10938")
def on_webinar_create_metadata(sender, **kwargs):
    """Create webinar's metadata after save"""

    if kwargs.get("instance"):

        # Create metadata
        webinar: Webinar = kwargs["instance"]
        WebinarMetadata.objects.get_or_create(webinar=webinar)

        # Add to aggregate
        aggregate = get_or_create_aggregate(webinar)
        aggregate_add_webinar(aggregate, webinar)

        # TODO: To nie dziala bo nie ma jeszcze webinar.categories.all()
        # for category in webinar.categories.all():
        #     aggregate_add_category(aggregate, category)

        # Update conflicts
        aggregate_update_conflicts(aggregate)
