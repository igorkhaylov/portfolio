"""Translated fields (django-modeltranslation).

Every user-facing string that lives in the database is registered here, so the same
content can be maintained in Russian and English from the admin (or Rosetta).
"""

from modeltranslation.translator import TranslationOptions, register

from .models import (
    Course,
    Education,
    Experience,
    Profile,
    Project,
    ProjectCategory,
    ProjectImage,
    Skill,
    SkillGroup,
    SocialLink,
)


@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ("headline", "role", "summary", "bio", "location", "meta_description", "meta_keywords")


@register(SocialLink)
class SocialLinkTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Experience)
class ExperienceTranslationOptions(TranslationOptions):
    fields = ("position", "company", "location", "description", "highlights")


@register(Education)
class EducationTranslationOptions(TranslationOptions):
    fields = ("institution", "degree", "speciality", "description", "highlights")


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ("title", "provider", "description", "highlights")


@register(SkillGroup)
class SkillGroupTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Skill)
class SkillTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(ProjectCategory)
class ProjectCategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ("title", "summary", "description", "role", "client", "highlights")


@register(ProjectImage)
class ProjectImageTranslationOptions(TranslationOptions):
    fields = ("caption",)
