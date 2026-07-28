__all__ = ("Profile", "SocialLink")

from django.core.cache import cache
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from stdimage.models import StdImageField

from common.models import BaseModel, TimestampMixin

PROFILE_CACHE_KEY = "portfolio:current_profile_id"
PROFILE_CACHE_TIMEOUT = 60 * 60


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

        Every page needs it, so the resolved id is cached; the row itself is fetched
        fresh (its social links are prefetched) to keep edits visible immediately.
        """
        profile_id = cache.get(PROFILE_CACHE_KEY)
        if profile_id is not None:
            profile = self.with_social_links().filter(pk=profile_id, is_active=True).first()
            if profile is not None:
                return profile

        profile = self.active().with_social_links().first()
        if profile is not None:
            cache.set(PROFILE_CACHE_KEY, profile.pk, PROFILE_CACHE_TIMEOUT)
        return profile


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
    bio = models.TextField(_("Biography"), blank=True, help_text=_("Longer text for the resume block."))

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(PROFILE_CACHE_KEY)

    @property
    def headline_items(self) -> list[str]:
        """Headline split for the typed.js rotation in the hero."""
        return [item.strip() for item in self.headline.split(",") if item.strip()]

    @property
    def years_of_experience(self) -> int | None:
        if not self.career_started_at:
            return None
        return max(timezone.now().year - self.career_started_at, 0)


class SocialLink(BaseModel):
    """A link in the sidebar (Telegram, GitHub, ...). Icon is a boxicons class name."""

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
        default="bx bxl-link",
        help_text=_("Boxicons class, e.g. bxl-telegram, bxl-github, bxl-linkedin."),
    )
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta(BaseModel.Meta):
        verbose_name = _("Social link")
        verbose_name_plural = _("Social links")

    def __str__(self) -> str:
        return self.title

    @property
    def icon_class(self) -> str:
        """Boxicons needs the `bx` base class; accept both `bxl-github` and the full form."""
        icon = self.icon.strip()
        return icon if icon.startswith("bx ") else f"bx {icon}"
