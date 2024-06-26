from datetime import datetime
from urllib.parse import urljoin

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def microservice_title():
    return settings.MICROSERVICE_TITLE


@register.simple_tag
def github_link():
    return settings.GITHUB_URL


@register.filter(name="date_time")
def date(value: str):
    """2021-04-11T18:02:37.066850Z"""
    time = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    return time.strftime("%b %dth, %Y")


@register.simple_tag
def timezone_cookie_name():
    return getattr(settings, "TIMEZONE_COOKIE_NAME", "timezone")


@register.simple_tag
def chat_site_init():
    if settings.BACKEND_SITE == "http://localhost:8008":
        return "http://localhost:8010/init/"
    return "https://www.chat-microservice.com/init/"


@register.simple_tag
def backend_site():
    return urljoin(settings.BACKEND_SITE, "/")


@register.simple_tag
def google_captcha():
    return settings.GOOGLE_CAPTCHA_SITE_SECRET_KEY
