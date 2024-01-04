class BlacklistReason:
    MANUAL = "MANUAL"
    AGGRESSOR = "AGGRESSOR"
    PLEADING = "PLEADING"


BLACKLIST_REASON_CHOICES = [
    (BlacklistReason.MANUAL, "Zablokowano ręcznie"),
    (BlacklistReason.AGGRESSOR, "Agresor"),
    (BlacklistReason.PLEADING, "Grzeczna prośba"),
]
