from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.urls import path, reverse

from core.models import Webinar


class WebinarSitemap(sitemaps.Sitemap):
    """Webinar sitemap"""

    priority = 0.6
    changefreq = "daily"

    def items(self):
        """Items"""
        return Webinar.manager.all()

    def location(self, item: Webinar):
        """Location"""
        return reverse("core:webinar_program_page", kwargs={"slug": item.slug})

    def lastmod(self, item: Webinar):
        """Last modified"""
        return item.updated_at


sitemaps = {
    "webinar": WebinarSitemap,
}

sitemap_xml_path = path(
    "sitemap.xml",
    sitemap,
    {"sitemaps": sitemaps},
    name="django.contrib.sitemaps.views.sitemap",
)
