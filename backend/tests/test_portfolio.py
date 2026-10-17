from datetime import date

from django.core.management import call_command
from django.urls import reverse

import pytest

from portfolio.models import (
    Experience,
    FocusArea,
    Profile,
    Project,
    ProjectCategory,
    Skill,
    SkillGroup,
    Stat,
)


@pytest.fixture
def profile(db):
    return Profile.objects.create(
        full_name="Igor Khaylov",
        headline="Backend Developer, Python Developer",
        role="Backend Developer",
        email="owner@example.com",
        location="Samarkand",
        career_started_at=2019,
    )


@pytest.fixture
def project(db):
    category = ProjectCategory.objects.create(title="Web", slug="web")
    project = Project.objects.create(title="Corporate site", slug="corporate-site", category=category)
    group = SkillGroup.objects.create(title="Backend")
    project.skills.add(Skill.objects.create(name="Django", group=group))
    return project


class TestProfile:
    def test_current_returns_active_profile(self, profile):
        assert Profile.objects.current() == profile

    def test_current_ignores_inactive(self, profile):
        profile.is_active = False
        profile.save()
        assert Profile.objects.current() is None

    def test_headline_items_split(self, profile):
        assert profile.headline_items == ["Backend Developer", "Python Developer"]

    def test_years_of_experience(self, profile):
        assert profile.years_of_experience >= 6


class TestResume:
    def test_period_for_ongoing_entry(self, db):
        item = Experience.objects.create(position="Freelance", started_at=date(2020, 1, 1), is_current=True)
        assert "2020" in item.period

    def test_period_for_closed_entry(self, db):
        item = Experience.objects.create(position="Operator", started_at=date(2015, 1, 1), finished_at=date(2018, 1, 1))
        assert item.period == "2015 — 2018"

    def test_highlight_list_skips_blank_lines(self, db):
        item = Experience.objects.create(position="Freelance", highlights="First\n\n  Second  \n")
        assert item.highlight_list == ["First", "Second"]


class TestProjects:
    def test_used_categories_exclude_empty(self, project):
        ProjectCategory.objects.create(title="Empty", slug="empty")
        assert list(ProjectCategory.objects.published().used()) == [project.category]

    def test_absolute_url(self, project):
        assert project.get_absolute_url().endswith("/projects/corporate-site/")


class TestPages:
    def test_index_renders(self, client, profile, project):
        response = client.get(reverse("portfolio:index"))
        assert response.status_code == 200
        assert profile.full_name in response.content.decode()

    def test_index_renders_without_profile(self, client, db):
        """A fresh database must not 500 the front page."""
        assert client.get(reverse("portfolio:index")).status_code == 200

    def test_project_detail(self, client, profile, project):
        response = client.get(project.get_absolute_url())
        assert response.status_code == 200

    def test_unpublished_project_is_404(self, client, profile, project):
        project.is_published = False
        project.save()
        assert client.get(project.get_absolute_url()).status_code == 404

    def test_sitemap(self, client, project):
        response = client.get("/sitemap.xml")
        assert response.status_code == 200
        assert b"corporate-site" in response.content

    def test_robots(self, client):
        response = client.get("/robots.txt")
        assert response.status_code == 200
        assert b"Sitemap:" in response.content


class TestSeedCommand:
    def test_seed_is_idempotent(self, db):
        call_command("seed_portfolio", verbosity=0)
        first = (Profile.objects.count(), Experience.objects.count(), Skill.objects.count())
        call_command("seed_portfolio", verbosity=0)
        assert (Profile.objects.count(), Experience.objects.count(), Skill.objects.count()) == first
        assert Profile.objects.current() is not None

    def test_seed_removes_retired_projects(self, db):
        Project.objects.create(title="Old card", slug="react-and-project-templates")
        call_command("seed_portfolio", verbosity=0)
        assert not Project.objects.filter(slug="react-and-project-templates").exists()
        assert Project.objects.filter(slug__in=("react-template", "project-template")).count() == 2

    def test_seed_fills_every_section(self, db):
        call_command("seed_portfolio", verbosity=0)
        assert Stat.objects.for_hero().exists()
        assert Stat.objects.for_infrastructure().exists()
        assert FocusArea.objects.for_about().exists()
        assert FocusArea.objects.for_infrastructure().exists()
        assert Project.objects.published().featured().exists()
        # Every project has a stack: an unknown skill name in the seed raises instead.
        assert not Project.objects.filter(skills__isnull=True).exists()

    def test_seeded_site_renders_in_both_languages(self, client, db):
        call_command("seed_portfolio", verbosity=0)
        ru = client.get("/ru/").content.decode()
        en = client.get("/en/").content.decode()
        assert "Игорь Хайлов" in ru
        assert "Igor Khaylov" in en
        for slug in ("splay", "iccu-tickets", "django-template"):
            assert f"/projects/{slug}/" in ru
        for project in Project.objects.published():
            assert client.get(project.get_absolute_url()).status_code == 200


class TestShowcase:
    def test_stats_are_split_by_section(self, db):
        hero = Stat.objects.create(value="~100", label="servers")
        infra = Stat.objects.create(section=Stat.Section.INFRASTRUCTURE, value="10", label="hypervisors")
        assert list(Stat.objects.for_hero()) == [hero]
        assert list(Stat.objects.for_infrastructure()) == [infra]

    def test_focus_area_stack_list(self, db):
        area = FocusArea.objects.create(title="Backend", stack="Python, Django , ,PostgreSQL")
        assert area.stack_list == ["Python", "Django", "PostgreSQL"]

    def test_index_shows_project_status_and_filters(self, client, profile, project):
        project.status = Project.Status.ARCHIVED
        project.save()
        html = client.get(reverse("portfolio:index")).content.decode()
        assert 'data-filter="web"' in html
        assert "status--archived" in html
