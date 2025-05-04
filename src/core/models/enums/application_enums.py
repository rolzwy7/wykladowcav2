class ApplicationStatus:
    """Application status"""

    INIT = "INIT"
    SENT = "SENT"
    RESIGNATION = "RESIGNATION"
    PAYED = "PAYED"


class ApplicationMoveStatus:
    """Application move status"""

    INIT = "INIT"
    RESIGNATION = "RESIGNATION"
    ACCEPTED = "ACCEPTED"
    ACCEPTED_WITH_DISCOUNT = "ACCEPTED_WITH_DISCOUNT"


class SaleRecordingApplicationStatus:
    """Application status"""

    INIT = "INIT"
    CANCELED_BY_SYSTEM = "CANCELED_BY_SYSTEM"
    WAITING_FOR_PAYMENT = "WAITING_FOR_PAYMENT"
    PAYED = "PAYED"
