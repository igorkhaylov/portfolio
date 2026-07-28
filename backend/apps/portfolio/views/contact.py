__all__ = ("ContactCreateView",)

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView

from common.request import get_ip_from_request
from portfolio.forms import ContactForm
from portfolio.models import ContactMessage

SUCCESS_MESSAGE = _("Your message has been sent. Thank you!")
ERROR_MESSAGE = _("Please check the form and try again.")


class ContactCreateView(FormView):
    """Handles the contact form.

    Answers JSON to `fetch` (the front-end path) and falls back to a redirect with a
    flash message when JavaScript is unavailable.
    """

    form_class = ContactForm
    http_method_names = ("post",)

    @property
    def is_ajax(self) -> bool:
        return self.request.headers.get("x-requested-with") == "XMLHttpRequest"

    def get_success_url(self) -> str:
        return f"{reverse('portfolio:index')}#contact"

    def form_valid(self, form):
        ContactMessage.objects.submit(
            ip=get_ip_from_request(self.request),
            user_agent=self.request.META.get("HTTP_USER_AGENT", ""),
            **{field: form.cleaned_data[field] for field in form.Meta.fields},
        )
        if self.is_ajax:
            return JsonResponse({"ok": True, "message": str(SUCCESS_MESSAGE)})
        messages.success(self.request, SUCCESS_MESSAGE)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.is_ajax:
            # get_json_data() gives a stable {field: [{message, code}]} contract.
            return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)
        messages.error(self.request, ERROR_MESSAGE)
        return HttpResponseRedirect(self.get_success_url())
