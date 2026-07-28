from django.http import HttpRequest

from .models import Profile


def profile(request: HttpRequest) -> dict:
    """Expose the site owner to every template — the sidebar renders on all pages."""
    return {"profile": Profile.objects.current()}
