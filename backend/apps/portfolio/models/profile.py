__all__ = ("Profile", "SocialLink")

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from stdimage.models import StdImageField

from common.models import BaseModel, TimestampMixin


class ProfileQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def with_social_links(self):
        return self.prefetch_related(
            models.Prefetch(
                "social_links",
                queryset=SocialLink.objects.filter(is_active=True),
            )
        )


class ProfileManager(models.Manager.from_queryset(ProfileQuerySet)):
    def current(self) -> "Profile | None":
        """The single active profile the whole site renders from.

        Not cached: the cache is per gunicorn worker (no Redis in the stack), so a cached
        value would keep serving stale data from the workers that did not save the edit.
        It is one indexed query per page.
        """
        return self.active().with_social_links().first()


class Profile(TimestampMixin):
    """Owner of the site: everything shown in the sidebar, hero and about blocks."""

    full_name = models.CharField(_("Full name"), max_length=150)
    headline = models.CharField(
        _("Headline"),
        max_length=255,
        blank=True,
        help_text=_("Rotating job titles in the hero, comma-separated: Backend Developer, Python Developer"),
    )
    role = models.CharField(
        _("Role"),
        max_length=150,
        blank=True,
        help_text=_("Short title under the About heading, e.g. Python Developer & Web Developer."),
    )
    summary = models.TextField(_("Summary"), blank=True, help_text=_("Two or three sentences for the About block."))
    bio = models.TextField(_("Biography"), blank=True, help_text=_("Longer text for the About block."))
    now = models.TextField(
        _("Now"),
        blank=True,
        help_text=_("What I am working on right now — one item per line."),
    )

    location = models.CharField(_("Location"), max_length=150, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    phone = models.CharField(_("Phone"), max_length=32, blank=True)
    birth_date = models.DateField(_("Date of birth"), blank=True, null=True)
    career_started_at = models.PositiveSmallIntegerField(
        _("Career start year"),
        blank=True,
        null=True,
        help_text=_("Used to render years of experience automatically."),
    )
    is_available_for_hire = models.BooleanField(_("Open to work"), default=True)

    avatar = StdImageField(_("Avatar"), upload_to="profile/avatar/", blank=True, null=True)
    hero_image = StdImageField(_("Hero background"), upload_to="profile/hero/", blank=True, null=True)
    resume_file = models.FileField(_("CV file"), upload_to="profile/cv/", blank=True, null=True)

    meta_description = models.CharField(
        _("Meta description"),
        max_length=300,
        blank=True,
        help_text=_('Used in <meta name="description"> and social previews.'),
    )
    meta_keywords = models.CharField(_("Meta keywords"), max_length=300, blank=True)

    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("The site renders the first active profile."),
    )

    objects = ProfileManager()

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profile")
        ordering = ("-is_active", "-updated_at")

    def __str__(self) -> str:
        return self.full_name

    @property
    def headline_items(self) -> list[str]:
        """Headline split into the role tags shown above the name in the hero."""
        return [item.strip() for item in self.headline.split(",") if item.strip()]

    @property
    def years_of_experience(self) -> int | None:
        if not self.career_started_at:
            return None
        return max(timezone.now().year - self.career_started_at, 0)


class SocialLink(BaseModel):
    """A contact link (Telegram, GitHub, ...). Icon is a name from the site's SVG sprite."""

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="social_links",
        verbose_name=_("Profile"),
    )
    title = models.CharField(_("Title"), max_length=50)
    url = models.URLField(_("URL"))
    icon = models.CharField(
        _("Icon"),
        max_length=50,
        default="link",
        help_text=_("Icon name from the site sprite: telegram, github, link."),
    )
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta(BaseModel.Meta):
        verbose_name = _("Social link")
        verbose_name_plural = _("Social links")

    def __str__(self) -> str:
        return self.title
