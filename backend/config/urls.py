"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.http import HttpResponse, JsonResponse
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from portfolio.sitemaps import sitemaps

APP_NAME = settings.APP_NAME


def robots_txt(request) -> HttpResponse:
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /rosetta/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


admin.site.site_title = _("%(app_name)s site admin") % {"app_name": APP_NAME}
admin.site.site_header = _("%(app_name)s administration") % {"app_name": APP_NAME}
admin.site.index_title = _("Site administration")
admin.site.enable_nav_sidebar = True
admin.site.empty_value_display = "-"

urlpatterns = [
    path(
        "healthcheck/",
        lambda request: JsonResponse({"status": "ok"}),
        name="healthcheck",
    ),
    # Language switcher POSTs here (django.conf.urls.i18n); must stay outside
    # i18n_patterns so it is reachable under any active language.
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "sitemap.xml",
        sitemap_view,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", robots_txt, name="robots_txt"),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("portfolio.urls", namespace="portfolio")),
)


if settings.ENVIRONMENT == "dev":
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [path("rosetta/", include("rosetta.urls"))]
