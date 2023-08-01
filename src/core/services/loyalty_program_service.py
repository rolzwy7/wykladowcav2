from random import randint

from core.models import LoyaltyProgram


class LoyaltyProgramService:
    """Loyality program service"""

    def __init__(self, user) -> None:
        self.user = user

    def loyalty_program_exists_for_user(self) -> bool:
        """Check if loyalty program exists for given user"""
        return LoyaltyProgram.manager.filter(user=self.user).exists()

    @staticmethod
    def generate_unused_ref_number() -> str:
        """Get unused ref number"""
        for _ in range(1_000):
            candidate = str(randint(10_000, 99_999))
            exists = LoyaltyProgram.manager.filter(
                ref_number=candidate
            ).exists()
            if not exists:
                return candidate
        return "1234567"  # low probability case

    def get_or_create_loyalty_program(self):
        """Get or create loyality program for given user"""
        program_exists = self.loyalty_program_exists_for_user()

        if program_exists:
            loyalty_program = LoyaltyProgram.manager.get(user=self.user)
        else:
            loyalty_program = LoyaltyProgram(
                ref_number=self.generate_unused_ref_number(),
                user=self.user,
            )
            loyalty_program.save()

        return loyalty_program
