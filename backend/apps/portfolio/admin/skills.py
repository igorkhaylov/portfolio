__all__ = ("SkillAdmin", "SkillGroupAdmin")

from django.contrib import admin

from modeltranslation.admin import TranslationAdmin, TranslationTabularInline

from portfolio.models import Skill, SkillGroup


class SkillInline(TranslationTabularInline):
    model = Skill
    extra = 1
    fields = ("rank", "name", "level", "icon", "is_featured", "is_published")


@admin.register(SkillGroup)
class SkillGroupAdmin(TranslationAdmin):
    inlines = (SkillInline,)
    list_display = ("title", "rank", "is_published")
    list_editable = ("rank", "is_published")
    search_fields = ("title",)  # required by Skill.group autocomplete


@admin.register(Skill)
class SkillAdmin(TranslationAdmin):
    list_display = ("name", "group", "level", "rank", "is_featured", "is_published")
    list_editable = ("level", "rank", "is_featured", "is_published")
    list_filter = ("group", "is_featured", "is_published")
    search_fields = ("name",)
    autocomplete_fields = ("group",)
