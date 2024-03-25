"""Mailing resignations service"""

# flake8: noqa=E501

from typing import Optional

from core.models.mailing import MailingTracking, MailingTrackingManager


class MailingTrackingService:
    """Mailing tracking service"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_or_create_tracking(email: str) -> str:
        """Create tracking for given email"""
        manager = MailingTrackingManager()
        tracking_code = manager.get_or_create_tracking(email)["_id"]
        manager.close()
        return tracking_code

    @staticmethod
    def get_by_code(code: str) -> Optional[MailingTracking]:
        """Get by resignation code"""
        manager = MailingTrackingManager()
        document = manager.get_tracking_by_code(code)
        manager.close()
        if document:
            return MailingTracking(email=document["email"])
        return None

    @staticmethod
    def get_by_email(email: str) -> Optional[MailingTracking]:
        """Get by resignation code"""
        manager = MailingTrackingManager()
        document = manager.get_tracking_by_email(email)
        manager.close()
        if document:
            return MailingTracking(email=document["email"])
        return None
