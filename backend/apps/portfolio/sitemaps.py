from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Project


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "monthly"
    i18n = True

    def items(self) -> list[str]:
        return ["portfolio:index"]

    def location(self, item: str) -> str:
        return reverse(item)


class ProjectSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"
    i18n = True

    def items(self):
        return Project.objects.published()

    def lastmod(self, obj: Project):
        return obj.updated_at


sitemaps = {
    "static": StaticViewSitemap,
    "projects": ProjectSitemap,
}
