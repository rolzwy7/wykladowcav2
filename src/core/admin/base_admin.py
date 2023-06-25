from django.contrib import admin

from core.models import (
    User,
    WebinarApplication,
    WebinarApplicationSubmitter,
    WebinarParticipant,
)

admin.site.register(User)
admin.site.register(WebinarParticipant)
admin.site.register(WebinarApplication)
admin.site.register(WebinarApplicationSubmitter)
