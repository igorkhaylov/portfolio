__all__ = ("ContactMessageAdmin",)

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from portfolio.models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "ip", "user_agent", "created_at", "updated_at")
    date_hierarchy = "created_at"
    actions = ("mark_read", "mark_unread")

    def has_add_permission(self, request) -> bool:
        # Messages only ever arrive through the public form.
        return False

    @admin.action(description=_("Mark selected messages as read"))
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description=_("Mark selected messages as unread"))
    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)
