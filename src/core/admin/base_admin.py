from django.contrib import admin

from core.models import (
    User,
    WebinarApplication,
    WebinarApplicationSubmitter,
    WebinarEventlog,
    WebinarParticipant,
)

admin.site.register(User)
admin.site.register(WebinarEventlog)
admin.site.register(WebinarParticipant)
admin.site.register(WebinarApplication)
admin.site.register(WebinarApplicationSubmitter)
