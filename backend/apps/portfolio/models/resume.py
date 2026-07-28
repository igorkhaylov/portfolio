__all__ = ("Course", "Education", "Experience")

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

from .mixins import HighlightsMixin


class PeriodQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)


class PeriodMixin(models.Model):
    """Shared shape of every resume entry: a visible date range plus a publish flag."""

    started_at = models.DateField(_("Start date"), blank=True, null=True)
    finished_at = models.DateField(
        _("End date"),
        blank=True,
        null=True,
        help_text=_("Leave empty for an ongoing period."),
    )
    is_current = models.BooleanField(_("Ongoing"), default=False)
    is_published = models.BooleanField(_("Published"), default=True)

    class Meta:
        abstract = True

    @property
    def period(self) -> str:
        """`2020 — Present` / `2015 — 2018` / `2014`, rendered from the stored dates."""
        start = self.started_at.year if self.started_at else None
        if self.is_current or (self.started_at and not self.finished_at):
            return _("%(start)s — Present") % {"start": start} if start else str(_("Present"))
        end = self.finished_at.year if self.finished_at else None
        if start and end and start != end:
            return f"{start} — {end}"
        return str(start or end or "")


class Experience(PeriodMixin, HighlightsMixin, BaseModel):
    """A job, a freelance period or teaching — anything that goes under Experience."""

    position = models.CharField(_("Position"), max_length=150)
    company = models.CharField(_("Company"), max_length=150, blank=True)
    location = models.CharField(_("Location"), max_length=150, blank=True)
    description = models.TextField(_("Description"), blank=True)
    company_url = models.URLField(_("Company URL"), blank=True)

    objects = PeriodQuerySet.as_manager()

    class Meta(BaseModel.Meta):
        verbose_name = _("Experience")
        verbose_name_plural = _("Experience")

    def __str__(self) -> str:
        return f"{self.position} — {self.company}" if self.company else self.position


class Education(PeriodMixin, HighlightsMixin, BaseModel):
    """Formal education: college, university, professional programs."""

    institution = models.CharField(_("Institution"), max_length=200)
    degree = models.CharField(_("Degree"), max_length=150, blank=True)
    speciality = models.CharField(_("Speciality"), max_length=150, blank=True)
    description = models.TextField(_("Description"), blank=True)

    objects = PeriodQuerySet.as_manager()

    class Meta(BaseModel.Meta):
        verbose_name = _("Education")
        verbose_name_plural = _("Education")

    def __str__(self) -> str:
        return f"{self.degree or self.speciality} — {self.institution}" if self.degree else self.institution


class Course(PeriodMixin, HighlightsMixin, BaseModel):
    """Self-education: online courses, certifications, bootcamps."""

    title = models.CharField(_("Title"), max_length=200)
    provider = models.CharField(_("Provider"), max_length=200, blank=True)
    description = models.TextField(_("Description"), blank=True)
    url = models.URLField(_("Certificate or course URL"), blank=True)

    objects = PeriodQuerySet.as_manager()

    class Meta(BaseModel.Meta):
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self) -> str:
        return self.title
