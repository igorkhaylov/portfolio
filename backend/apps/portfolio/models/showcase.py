__all__ = ("FocusArea", "Stat")

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

from .mixins import HighlightsMixin

# Names of the symbols in templates/includes/icons.html. Kept as a choice list so the
# admin cannot point a card at an icon the sprite does not have.
ICON_CHOICES = (
    ("code", _("Code")),
    ("server", _("Server")),
    ("layers", _("Layers")),
    ("database", _("Database")),
    ("activity", _("Activity")),
    ("cpu", _("CPU / GPU")),
    ("play", _("Video")),
    ("shield", _("Shield")),
    ("globe", _("Globe")),
    ("git", _("Git")),
    ("terminal", _("Terminal")),
    ("box", _("Package")),
)


class StatQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def for_hero(self):
        return self.published().filter(section=Stat.Section.HERO)

    def for_infrastructure(self):
        return self.published().filter(section=Stat.Section.INFRASTRUCTURE)


class Stat(BaseModel):
    """A headline number: "~100 servers", "290 TB of video"."""

    class Section(models.TextChoices):
        HERO = "hero", _("Hero")
        INFRASTRUCTURE = "infrastructure", _("Infrastructure")

    section = models.CharField(_("Section"), max_length=20, choices=Section.choices, default=Section.HERO)
    value = models.CharField(_("Value"), max_length=20, help_text=_("Shown large: 10, ~100, 1.4 PB."))
    label = models.CharField(_("Label"), max_length=100)
    note = models.CharField(_("Note"), max_length=200, blank=True, help_text=_("Small print under the label."))
    is_published = models.BooleanField(_("Published"), default=True)

    objects = StatQuerySet.as_manager()

    class Meta(BaseModel.Meta):
        verbose_name = _("Stat")
        verbose_name_plural = _("Stats")

    def __str__(self) -> str:
        return f"{self.value} {self.label}"


class FocusAreaQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def for_about(self):
        return self.published().filter(section=FocusArea.Section.ABOUT)

    def for_infrastructure(self):
        return self.published().filter(section=FocusArea.Section.INFRASTRUCTURE)


class FocusArea(HighlightsMixin, BaseModel):
    """A card: what I do (About) or what the infrastructure I run consists of."""

    class Section(models.TextChoices):
        ABOUT = "about", _("What I do")
        INFRASTRUCTURE = "infrastructure", _("Infrastructure")

    section = models.CharField(_("Section"), max_length=20, choices=Section.choices, default=Section.ABOUT)
    title = models.CharField(_("Title"), max_length=150)
    summary = models.TextField(_("Summary"), blank=True)
    icon = models.CharField(_("Icon"), max_length=20, choices=ICON_CHOICES, default="code")
    stack = models.CharField(
        _("Stack"),
        max_length=300,
        blank=True,
        help_text=_("Technologies shown as tags, comma-separated."),
    )
    is_published = models.BooleanField(_("Published"), default=True)

    objects = FocusAreaQuerySet.as_manager()

    class Meta(BaseModel.Meta):
        verbose_name = _("Focus area")
        verbose_name_plural = _("Focus areas")

    def __str__(self) -> str:
        return self.title

    @property
    def stack_list(self) -> list[str]:
        return [item.strip() for item in self.stack.split(",") if item.strip()]
