from core.models.mailing import MailingResignationManager


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
    def confirm_resignation(email: str) -> None:
        """Confirm resignation"""
        manager = MailingResignationManager()
        manager.mark_confirmed(email)
        manager.close()
