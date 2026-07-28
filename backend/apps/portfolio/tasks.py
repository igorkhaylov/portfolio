import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext as _

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def notify_new_contact_message(self, message_id: int) -> None:
    """Email the site owner about a new contact-form message."""
    from portfolio.models import ContactMessage, Profile

    message = ContactMessage.objects.filter(pk=message_id).first()
    if message is None:
        logger.warning("contact_message_missing", extra={"message_id": message_id})
        return

    profile = Profile.objects.current()
    recipient = getattr(settings, "CONTACT_NOTIFY_EMAIL", "") or (profile.email if profile else "")
    if not recipient:
        logger.info("contact_message_notification_skipped_no_recipient", extra={"message_id": message_id})
        return

    subject = _("New message from %(name)s") % {"name": message.name}
    body = _("Name: %(name)s\nEmail: %(email)s\nSubject: %(subject)s\n\n%(message)s") % {
        "name": message.name,
        "email": message.email,
        "subject": message.subject or "-",
        "message": message.message,
    }

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
    except Exception as exc:
        logger.exception("contact_message_notification_failed", extra={"message_id": message_id})
        raise self.retry(exc=exc) from exc
