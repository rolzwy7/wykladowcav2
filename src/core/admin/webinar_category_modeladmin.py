# flake8: noqa:DJ07

from django.contrib.admin import ModelAdmin, register
from django.forms import ModelForm
from tinymce.widgets import TinyMCE

from core.models import WebinarCategory


class WebinarCategoryModelAdminForm(ModelForm):
    """Webinar Category Model Admin Form"""

    class Meta:
        model = WebinarCategory
        fields = "__all__"
        widgets = {"about_html": TinyMCE(attrs={"cols": 80, "rows": 30})}


@register(WebinarCategory)
class WebinarCategoryModelAdmin(ModelAdmin):
    """Webinar Category Model Admin"""

    form = WebinarCategoryModelAdminForm
    list_display = [
        "name",
        "parent",
        "visible",
        "is_homepage_category",
        "slug",
        "order",
    ]
