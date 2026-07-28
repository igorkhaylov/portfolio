__all__ = ("ProfileAdmin", "SocialLinkInline")

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from portfolio.models import Profile, SocialLink


class SocialLinkInline(TranslationTabularInline):
    model = SocialLink
    extra = 1
    fields = ("rank", "title", "url", "icon", "is_active")


@admin.register(Profile)
class ProfileAdmin(TranslationAdmin):
    inlines = (SocialLinkInline,)
    list_display = ("full_name", "role", "location", "is_available_for_hire", "is_active", "updated_at")
    list_editable = ("is_active",)
    readonly_fields = ("avatar_preview", "created_at", "updated_at")
    save_on_top = True
    fieldsets = (
        (None, {"fields": ("full_name", "headline", "role", "is_active")}),
        (_("About"), {"fields": ("summary", "bio", "career_started_at", "is_available_for_hire")}),
        (_("Contacts"), {"fields": ("location", "email", "phone", "birth_date")}),
        (_("Media"), {"fields": (("avatar", "avatar_preview"), "hero_image", "resume_file")}),
        (_("SEO"), {"fields": ("meta_description", "meta_keywords"), "classes": ("collapse",)}),
        (_("Service"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description=_("Preview"))
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" height="150" />', obj.avatar.small.url)
        return "-"
