__all__ = ("FocusAreaAdmin", "StatAdmin")

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin

from portfolio.models import FocusArea, Stat


@admin.register(Stat)
class StatAdmin(TranslationAdmin):
    list_display = ("value", "label", "section", "rank", "is_published")
    list_editable = ("rank", "is_published")
    list_filter = ("section", "is_published")
    search_fields = ("value", "label")


@admin.register(FocusArea)
class FocusAreaAdmin(TranslationAdmin):
    list_display = ("title", "section", "icon", "rank", "is_published")
    list_editable = ("rank", "is_published")
    list_filter = ("section", "is_published")
    search_fields = ("title", "summary", "stack")
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("section", "title", "icon", "summary")}),
        (_("Details"), {"fields": ("highlights", "stack")}),
        (_("Display"), {"fields": ("rank", "is_published")}),
    )
