from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Contact form on the front page.

    `website` is a honeypot: bots fill every field they find, humans never see it.
    """

    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ("name", "email", "subject", "message")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Your name")}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": _("Your email")}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": _("Subject")}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 8, "placeholder": _("Message")}),
        }

    def clean_website(self) -> str:
        if self.cleaned_data.get("website"):
            raise forms.ValidationError(_("Spam detected."))
        return ""

    def clean_message(self) -> str:
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError(_("Please write at least 10 characters."))
        return message
