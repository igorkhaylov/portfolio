__all__ = ("CourseAdmin", "EducationAdmin", "ExperienceAdmin")

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin

from portfolio.models import Course, Education, Experience


class ResumeEntryAdmin(TranslationAdmin):
    """Shared admin shape for the three resume sections."""

    list_editable = ("rank", "is_published")
    list_filter = ("is_published", "is_current")
    date_hierarchy = "started_at"
    save_on_top = True

    class Media:
        # Vertically stacked language tabs read better for long translated text.
        css = {"screen": ("modeltranslation/css/tabbed_translation_fields.css",)}
        js = (
            "modeltranslation/js/force_jquery.js",
            "modeltranslation/js/tabbed_translation_fields.js",
        )


@admin.register(Experience)
class ExperienceAdmin(ResumeEntryAdmin):
    list_display = ("position", "company", "period", "rank", "is_published")
    search_fields = ("position", "company", "description")
    fieldsets = (
        (None, {"fields": ("position", "company", "company_url", "location")}),
        (_("Period"), {"fields": (("started_at", "finished_at"), "is_current")}),
        (_("Content"), {"fields": ("description", "highlights")}),
        (_("Display"), {"fields": ("rank", "is_published")}),
    )


@admin.register(Education)
class EducationAdmin(ResumeEntryAdmin):
    list_display = ("institution", "degree", "speciality", "period", "rank", "is_published")
    search_fields = ("institution", "degree", "speciality")
    fieldsets = (
        (None, {"fields": ("institution", "degree", "speciality")}),
        (_("Period"), {"fields": (("started_at", "finished_at"), "is_current")}),
        (_("Content"), {"fields": ("description", "highlights")}),
        (_("Display"), {"fields": ("rank", "is_published")}),
    )


@admin.register(Course)
class CourseAdmin(ResumeEntryAdmin):
    list_display = ("title", "provider", "period", "rank", "is_published")
    search_fields = ("title", "provider")
    fieldsets = (
        (None, {"fields": ("title", "provider", "url")}),
        (_("Period"), {"fields": (("started_at", "finished_at"), "is_current")}),
        (_("Content"), {"fields": ("description", "highlights")}),
        (_("Display"), {"fields": ("rank", "is_published")}),
    )
