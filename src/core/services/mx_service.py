from dns.resolver import NXDOMAIN, NoAnswer, query


class MxService:
    """Service for performing MX check"""

    def __init__(self) -> None:
        pass

    def has_domain_mx_record(self, domain: str):
        """Check if domain has MX record

        Args:
            domain (str): domain to be checked

        Returns:
            bool: True if MX present, False otherwise
        """
        try:
            answers = query(domain, "MX")
            return bool(answers)
        except (NoAnswer, NXDOMAIN):
            return False
        except Exception as exception:  # TODO: logger
            return False

    def has_email_mx_record(self, email: str):
        """Check if email's domain has MX record

        Args:
            email (str): email to be checked

        Returns:
            bool: True if MX present, False otherwise
        """
        _, domain = email.split("@")
        return self.has_domain_mx_record(domain)
