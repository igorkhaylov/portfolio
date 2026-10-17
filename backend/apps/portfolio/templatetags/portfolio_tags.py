from django import template
from django.urls import translate_url

register = template.Library()


@register.simple_tag(takes_context=True)
def switch_language_url(context, language_code: str) -> str:
    """URL of the current page in another language.

    Replaces the old string-replace hack (`path.replace("ru", "en")`, which also
    mangled any 'ru' inside a slug) with Django's own resolver-aware helper.
    """
    request = context.get("request")
    if request is None:
        return "/"
    return translate_url(request.get_full_path(), language_code)


@register.filter
def split_lines(value: str) -> list[str]:
    """Render a textarea field as a list: `{% for item in obj.field|split_lines %}`."""
    if not value:
        return []
    return [line.strip() for line in value.splitlines() if line.strip()]


@register.filter
def bare_url(value: str) -> str:
    """`https://splay.uz/` -> `splay.uz`: a link label without the scheme noise."""
    if not value:
        return ""
    for prefix in ("https://", "http://"):
        if value.startswith(prefix):
            value = value[len(prefix) :]
            break
    return value.removeprefix("www.").rstrip("/")
