from datetime import date

from django.core import mail
from django.urls import reverse

import pytest

from portfolio.models import ContactMessage, Experience, Profile, Project, ProjectCategory, Skill, SkillGroup


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


class TestContactForm:
    payload = {
        "name": "Client",
        "email": "client@example.com",
        "subject": "Website",
        "message": "I would like to order a website, please call me back.",
    }

    def test_submit_stores_message_and_sends_email(self, client, profile):
        response = client.post(
            reverse("portfolio:contact"),
            self.payload,
            headers={"x-requested-with": "XMLHttpRequest"},
        )
        assert response.status_code == 200
        assert response.json()["ok"] is True

        message = ContactMessage.objects.get()
        assert message.email == self.payload["email"]
        # Celery runs eagerly in tests, so the notification is already in the outbox.
        assert len(mail.outbox) == 1
        assert profile.email in mail.outbox[0].to

    def test_short_message_is_rejected(self, client, profile):
        response = client.post(
            reverse("portfolio:contact"),
            {**self.payload, "message": "hi"},
            headers={"x-requested-with": "XMLHttpRequest"},
        )
        assert response.status_code == 400
        assert "message" in response.json()["errors"]
        assert not ContactMessage.objects.exists()

    def test_honeypot_blocks_bots(self, client, profile):
        response = client.post(
            reverse("portfolio:contact"),
            {**self.payload, "website": "http://spam.example"},
            headers={"x-requested-with": "XMLHttpRequest"},
        )
        assert response.status_code == 400
        assert not ContactMessage.objects.exists()

    def test_non_ajax_submit_redirects(self, client, profile):
        response = client.post(reverse("portfolio:contact"), self.payload)
        assert response.status_code == 302
        assert ContactMessage.objects.count() == 1


class TestSeedCommand:
    def test_seed_is_idempotent(self, db):
        from django.core.management import call_command

        call_command("seed_portfolio", verbosity=0)
        first = (Profile.objects.count(), Experience.objects.count(), Skill.objects.count())
        call_command("seed_portfolio", verbosity=0)
        assert (Profile.objects.count(), Experience.objects.count(), Skill.objects.count()) == first
        assert Profile.objects.current() is not None
