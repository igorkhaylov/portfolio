__all__ = ("ProjectAdmin", "ProjectCategoryAdmin")

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from portfolio.models import Project, ProjectCategory, ProjectImage, ProjectSkill


class ProjectImageInline(TranslationTabularInline):
    model = ProjectImage
    extra = 1
    fields = ("rank", "image", "preview", "caption")
    readonly_fields = ("preview",)

    @admin.display(description=_("Preview"))
    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html('<img src="{}" height="80" />', obj.image.thumbnail.url)
        return "-"


class ProjectSkillInline(admin.TabularInline):
    model = ProjectSkill
    extra = 1
    autocomplete_fields = ("skill",)
    verbose_name = _("Stack item")
    verbose_name_plural = _("Stack")


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(TranslationAdmin):
    list_display = ("title", "slug", "rank", "is_published")
    list_editable = ("rank", "is_published")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    inlines = (ProjectSkillInline, ProjectImageInline)
    list_display = ("title", "category", "client", "released_at", "rank", "is_featured", "is_published")
    list_editable = ("rank", "is_featured", "is_published")
    list_filter = ("category", "is_featured", "is_published")
    search_fields = ("title", "summary", "description", "client")
    autocomplete_fields = ("category",)
    # TranslationAdmin rewrites this to the default-language field (title_ru).
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("cover_preview", "created_at", "updated_at")
    date_hierarchy = "released_at"
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "summary")}),
        (_("Content"), {"fields": ("description", "highlights", "role", "client")}),
        (_("Media"), {"fields": (("cover", "cover_preview"),)}),
        (_("Links"), {"fields": ("project_url", "repository_url")}),
        (_("Display"), {"fields": ("released_at", "rank", "is_featured", "is_published")}),
        (_("Service"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description=_("Preview"))
    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" height="150" />', obj.cover.small.url)
        return "-"
