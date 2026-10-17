__all__ = ("IndexView", "ProjectDetailView")

from django.db.models import Prefetch
from django.views.generic import DetailView, TemplateView

from portfolio.models import (
    Course,
    Education,
    Experience,
    FocusArea,
    Project,
    ProjectCategory,
    Skill,
    SkillGroup,
    Stat,
)


class IndexView(TemplateView):
    """Single-page site: every section is rendered from the database."""

    template_name = "portfolio/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = list(Project.objects.published().full())
        context.update(
            hero_stats=Stat.objects.for_hero(),
            infra_stats=Stat.objects.for_infrastructure(),
            focus_areas=FocusArea.objects.for_about(),
            infra_areas=FocusArea.objects.for_infrastructure(),
            experiences=Experience.objects.published(),
            educations=Education.objects.published(),
            courses=Course.objects.published(),
            skill_groups=SkillGroup.objects.filter(is_published=True).prefetch_related(
                Prefetch("skills", queryset=Skill.objects.published().order_by("rank"))
            ),
            categories=ProjectCategory.objects.published().used(),
            featured_projects=[project for project in projects if project.is_featured],
            projects=projects,
        )
        return context


class ProjectDetailView(DetailView):
    """Project page with the image gallery."""

    template_name = "portfolio/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.published().full()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_projects"] = (
            Project.objects.published()
            .full()
            .filter(category_id=self.object.category_id)
            .exclude(pk=self.object.pk)[:3]
            if self.object.category_id
            else Project.objects.none()
        )
        return context
