"""
Sitemaps
"""

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# flake8: noqa=E501

from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.urls import path, reverse

from core.models import Lecturer, Webinar, WebinarAggregate, WebinarCategory


class HighPrioritySitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return [reverse("core:homepage")]

    def location(self, item):
        return item


class LowPrioritySitemap(sitemaps.Sitemap):
    priority = 0.3
    changefreq = "weekly"

    def items(self):
        return [
            reverse("core:login_page"),
            reverse("core:contact_page"),
            reverse("core:about_us_page"),
            reverse("core:webmap_page"),
            reverse("core:all_lecturers_list_page"),
        ]

    def location(self, item):
        return item


class WebinarSitemap(sitemaps.Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        """Items"""
        return Webinar.manager.get_visible_webinars()

    def location(self, item: Webinar):
        return reverse("core:webinar_program_page", kwargs={"slug": item.slug})

    def lastmod(self, item: Webinar):
        return item.updated_at


class WebinarAggregateSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        """Items"""
        return WebinarAggregate.manager.get_active_aggregates()

    def location(self, item: WebinarAggregate):
        return reverse("core:webinar_aggregate_page", kwargs={"slug": item.slug})

    def lastmod(self, item: WebinarAggregate):
        return item.updated_at


class LecturerSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        """Items"""
        return Lecturer.manager.get_lecturers_visible_on_page()

    def location(self, item: Lecturer):
        return reverse("core:lecturer_experience_page", kwargs={"slug": item.slug})

    def lastmod(self, item: Lecturer):
        return item.updated_at


class CategorySitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        """Items"""
        return WebinarCategory.manager.get_visible_categories()

    def location(self, item: WebinarCategory):
        return reverse("core:webinar_category_page", kwargs={"slug": item.slug})

    def lastmod(self, item: WebinarCategory):
        return item.updated_at


sitemaps = {
    "homepage": HighPrioritySitemap,
    "aggregate": WebinarAggregateSitemap,
    # "webinar": WebinarSitemap,
    "lecturer": LecturerSitemap,
    "category": CategorySitemap,
    "low_priority": LowPrioritySitemap,
}

sitemap_xml_path = path(
    "sitemap.xml",
    sitemap,
    {"sitemaps": sitemaps},
    name="django.contrib.sitemaps.views.sitemap",
)
