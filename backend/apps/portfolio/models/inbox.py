__all__ = ("ContactMessage",)

import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimestampMixin, UIDMixin

logger = logging.getLogger(__name__)


class ContactMessageQuerySet(models.QuerySet):
    def unread(self):
        return self.filter(is_read=False)


class ContactMessageManager(models.Manager.from_queryset(ContactMessageQuerySet)):
    def submit(self, *, ip: str | None = None, user_agent: str = "", **fields) -> "ContactMessage":
        """Store a message from the contact form and notify the owner.

        Notification failures must never break the visitor's submit, so the email is
        queued through Celery and a broker outage only degrades to a logged warning.
        """
        message = self.create(ip=ip, user_agent=user_agent[:500], **fields)

        from portfolio.tasks import notify_new_contact_message

        try:
            notify_new_contact_message.delay(message.pk)
        except Exception:
            logger.warning("contact_message_notification_not_queued", exc_info=True)
        return message


class ContactMessage(UIDMixin, TimestampMixin):
    """A message left in the contact form on the front page."""

    name = models.CharField(_("Name"), max_length=150)
    email = models.EmailField(_("Email"))
    subject = models.CharField(_("Subject"), max_length=200, blank=True)
    message = models.TextField(_("Message"))

    ip = models.GenericIPAddressField(_("IP address"), blank=True, null=True)
    user_agent = models.CharField(_("User agent"), max_length=500, blank=True)
    is_read = models.BooleanField(_("Read"), default=False)

    objects = ContactMessageManager()

    class Meta:
        verbose_name = _("Contact message")
        verbose_name_plural = _("Contact messages")
        ordering = ("-created_at", "-id")
        indexes = [models.Index(fields=["is_read", "-created_at"])]

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
