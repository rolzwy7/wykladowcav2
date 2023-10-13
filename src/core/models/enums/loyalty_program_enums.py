class LoyaltyProgramIncomeStatus:
    """Status loyalty program income"""

    PROCESSING = "PROCESSING"
    PAYABLE = "PAYABLE"
    VIOLATING = "VIOLATING"


class LoyaltyProgramPayoutStatus:
    """Status for loyalty program income request"""

    WAITING_FOR_CONFIRMATION = "WAITING_FOR_CONFIRMATION"
    PAYED = "PAYED"
    REFUSED = "REFUSED"
