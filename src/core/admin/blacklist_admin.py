"""
Blacklist admin
"""
from django.contrib.admin import ModelAdmin, register

from core.models.blacklist import (
    BlacklistedDomain,
    BlacklistedEmail,
    BlacklistedEmailTemporary,
    BlacklistedPhrase,
    BlacklistedPrefix,
)


@register(BlacklistedDomain)
class BlacklistedDomainModelAdmin(ModelAdmin):
    """BlacklistedDomainModelAdmin"""

    search_fields = ["domain"]
    list_display = ["domain", "created_at"]


@register(BlacklistedEmail)
class BlacklistedEmailModelAdmin(ModelAdmin):
    """BlacklistedEmailModelAdmin"""

    search_fields = ["email"]
    list_display = ["email", "reason", "created_at"]


@register(BlacklistedEmailTemporary)
class BlacklistedEmailTemporaryModelAdmin(ModelAdmin):
    """BlacklistedEmailTemporaryModelAdmin"""

    def is_expired(self, obj: BlacklistedEmailTemporary):
        """Calculated field `is_expired`"""
        return obj.is_expired

    search_fields = ["email"]
    list_display = ["email", "is_expired", "expires_at"]

    is_expired.boolean = True


@register(BlacklistedPhrase)
class BlacklistedPhraseModelAdmin(ModelAdmin):
    """BlacklistedPhraseModelAdmin"""

    search_fields = ["phrase"]
    list_display = ["phrase", "created_at"]


@register(BlacklistedPrefix)
class BlacklistedPrefixModelAdmin(ModelAdmin):
    """BlacklistedPrefixModelAdmin"""

    search_fields = ["prefix"]
    list_display = ["prefix", "created_at"]
