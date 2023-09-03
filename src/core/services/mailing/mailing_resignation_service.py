from typing import Optional

from core.models.mailing import MailingResignation, MailingResignationManager


class MailingResignationService:
    """Mailing resignation service"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_email_confirmed_resignation(email: str) -> bool:
        """Check if email is in confirmed resignations"""
        manager = MailingResignationManager()
        ret = manager.is_resignation(email)
        manager.close()
        return ret

    @staticmethod
    def get_or_create_resignation_code(email: str) -> str:
        """Create inactive resignation for email and return resignation code"""
        manager = MailingResignationManager()
        resignation_code = manager.get_or_create_resignation(email)["_id"]
        manager.close()
        return resignation_code

    @staticmethod
    def confirm_resignation_by_email(email: str) -> None:
        """Confirm resignation by email"""
        manager = MailingResignationManager()
        manager.mark_confirmed_by_email(email)
        manager.close()

    @staticmethod
    def get_by_resignation_code(code: str) -> Optional[MailingResignation]:
        """Get by resignation code"""
        manager = MailingResignationManager()
        document = manager.get_by_resignation_code(code)
        manager.close()
        if document:
            return MailingResignation(
                email=document["email"],
                confirmed=document["confirmed"],
            )
        else:
            return None

    @staticmethod
    def confirm_resignation_by_code(code: str) -> None:
        """Confirm resignation by code"""
        manager = MailingResignationManager()
        manager.mark_confirmed_by_code(code)
        manager.close()
