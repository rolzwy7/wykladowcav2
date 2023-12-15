"""
Lead service
"""

# flake8: noqa=E501

from typing import Optional

from django.http import HttpRequest

from core.models import LeadModel, WebinarCategory

from .ip_address_service import IpAddressService


class LeadService:
    """LeadService"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_or_create_lead(
        email: str,
        lead_source: str,
        /,
        *,
        request: Optional[HttpRequest] = None,
        categories: Optional[list[WebinarCategory]] = None,
    ) -> LeadModel:
        """Get or create lead for given email"""
        _lead, created = LeadModel.manager.get_or_create(email=email)
        lead: LeadModel = _lead

        # Set lead source only if created for the first time
        if created:
            lead.lead_source = lead_source
            lead.is_subscribed = True

        # Set ip address if request is set
        if request:
            lead.singup_ip_address = IpAddressService.get_client_ip(request)

        # Save above changes
        lead.save()

        # If categories are set then connect to preferences
        if categories:
            for category in categories:
                lead.preferences.add(category)

        return lead

    @staticmethod
    def apply_basic_data(lead: LeadModel, first_name: str, last_name: str, phone: str):
        """
        Apply basic lead data
        """
        lead.first_name = first_name
        lead.last_name = last_name
        lead.phone = phone
        lead.save()
