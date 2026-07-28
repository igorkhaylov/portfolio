__all__ = ("Skill", "SkillGroup")

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel


class SkillQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def featured(self):
        return self.filter(is_featured=True)

    def with_group(self):
        return self.select_related("group")


class SkillGroup(BaseModel):
    """A column of skills: Backend, Frontend, DevOps, Tools."""

    title = models.CharField(_("Title"), max_length=100)
    is_published = models.BooleanField(_("Published"), default=True)

    class Meta(BaseModel.Meta):
        verbose_name = _("Skill group")
        verbose_name_plural = _("Skill groups")

    def __str__(self) -> str:
        return self.title


class Skill(BaseModel):
    """A single technology. Doubles as the tag set for projects (see Project.skills)."""

    group = models.ForeignKey(
        SkillGroup,
        on_delete=models.SET_NULL,
        related_name="skills",
        verbose_name=_("Group"),
        blank=True,
        null=True,
    )
    name = models.CharField(_("Name"), max_length=100)
    level = models.PositiveSmallIntegerField(
        _("Level, %"),
        default=80,
        help_text=_("0-100, drives the progress bar width."),
    )
    icon = models.CharField(
        _("Icon"),
        max_length=50,
        blank=True,
        help_text=_("Boxicons class, e.g. bxl-python."),
    )
    is_featured = models.BooleanField(
        _("Featured"),
        default=False,
        help_text=_("Featured skills are shown in the About block."),
    )
    is_published = models.BooleanField(_("Published"), default=True)

    objects = SkillQuerySet.as_manager()

    class Meta(BaseModel.Meta):
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

    def __str__(self) -> str:
        return self.name
