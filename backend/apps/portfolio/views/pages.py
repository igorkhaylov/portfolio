__all__ = ("IndexView", "ProjectDetailView")

from django.views.generic import DetailView, TemplateView

from portfolio.forms import ContactForm
from portfolio.models import Course, Education, Experience, Project, ProjectCategory, SkillGroup


class IndexView(TemplateView):
    """Single-page site: every section is rendered from the database."""

    template_name = "portfolio/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            experiences=Experience.objects.published(),
            educations=Education.objects.published(),
            courses=Course.objects.published(),
            skill_groups=SkillGroup.objects.filter(is_published=True).prefetch_related("skills"),
            categories=ProjectCategory.objects.published().used(),
            projects=Project.objects.published().full(),
            contact_form=kwargs.get("contact_form") or ContactForm(),
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
            .with_category()
            .filter(category_id=self.object.category_id)
            .exclude(pk=self.object.pk)[:3]
            if self.object.category_id
            else Project.objects.none()
        )
        return context
