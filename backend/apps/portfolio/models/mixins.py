__all__ = ("HighlightsMixin",)

from django.db import models
from django.utils.translation import gettext_lazy as _


class HighlightsMixin(models.Model):
    """Bullet points stored as plain text — one line per item.

    Content is filled in by hand in the admin, so a textarea beats a related model:
    no inline formset for what is visually a `<ul>`. Templates iterate `highlight_list`.
    """

    highlights = models.TextField(
        _("Highlights"),
        blank=True,
        help_text=_("One bullet point per line. Blank lines are ignored."),
    )

    class Meta:
        abstract = True

    @property
    def highlight_list(self) -> list[str]:
        return [line.strip() for line in self.highlights.splitlines() if line.strip()]
