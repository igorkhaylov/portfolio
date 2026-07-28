__all__ = ("Project", "ProjectCategory", "ProjectImage", "ProjectSkill")

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from stdimage.models import StdImageField

from common.models import BaseModel

from .mixins import HighlightsMixin
from .skills import Skill


class ProjectCategoryQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def used(self):
        """Only categories that actually have a published project — an empty filter
        button in the portfolio grid matches nothing and looks broken."""
        return self.filter(projects__is_published=True).distinct()


class ProjectCategory(BaseModel):
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=100, unique=True)
    is_published = models.BooleanField(_("Published"), default=True)

    objects = ProjectCategoryQuerySet.as_manager()

    class Meta(BaseModel.Meta):
        verbose_name = _("Project category")
        verbose_name_plural = _("Project categories")

    def __str__(self) -> str:
        return self.title


class ProjectQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def featured(self):
        return self.filter(is_featured=True)

    def with_category(self):
        return self.select_related("category")

    def with_skills(self):
        return self.prefetch_related(models.Prefetch("skills", queryset=Skill.objects.published().order_by("rank")))

    def with_images(self):
        return self.prefetch_related(models.Prefetch("images", queryset=ProjectImage.objects.order_by("rank")))

    def full(self):
        """Everything a card or a detail page renders — one query per relation."""
        return self.with_category().with_skills().with_images()


class Project(HighlightsMixin, BaseModel):
    title = models.CharField(_("Title"), max_length=150)
    slug = models.SlugField(_("Slug"), max_length=150, unique=True)
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        related_name="projects",
        verbose_name=_("Category"),
        blank=True,
        null=True,
    )
    summary = models.CharField(_("Summary"), max_length=300, blank=True)
    description = models.TextField(_("Description"), blank=True)
    role = models.CharField(_("My role"), max_length=150, blank=True)
    client = models.CharField(_("Client"), max_length=150, blank=True)

    cover = StdImageField(_("Cover"), upload_to="projects/cover/", blank=True, null=True)
    project_url = models.URLField(_("Live URL"), blank=True)
    repository_url = models.URLField(_("Repository URL"), blank=True)

    skills = models.ManyToManyField(
        Skill,
        through="ProjectSkill",
        related_name="projects",
        verbose_name=_("Stack"),
        blank=True,
    )

    released_at = models.DateField(_("Release date"), blank=True, null=True)
    is_featured = models.BooleanField(_("Featured"), default=False)
    is_published = models.BooleanField(_("Published"), default=True)

    objects = ProjectQuerySet.as_manager()

    class Meta(BaseModel.Meta):
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        indexes = [models.Index(fields=["is_published", "rank"])]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})


class ProjectSkill(models.Model):
    """Explicit M2M table: leaves room for per-project stack details later."""

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="project_skills")

    class Meta:
        verbose_name = _("Project stack item")
        verbose_name_plural = _("Project stack")
        constraints = [
            models.UniqueConstraint(fields=["project", "skill"], name="unique_project_skill"),
        ]

    def __str__(self) -> str:
        return f"{self.project} — {self.skill}"


class ProjectImage(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("Project"),
    )
    image = StdImageField(_("Image"), upload_to="projects/gallery/")
    caption = models.CharField(_("Caption"), max_length=200, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = _("Project image")
        verbose_name_plural = _("Project images")

    def __str__(self) -> str:
        return self.caption or f"{self.project} #{self.pk}"
