from django import template
from django.utils import timezone

register = template.Library()


def custom_timesince(value):
    now = timezone.now()
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())
    diff = now - value
    if diff < timezone.timedelta(minutes=1):
        return "1m"
    elif diff < timezone.timedelta(hours=1):
        return str(int(diff.total_seconds() / 60)) + "m"
    elif diff < timezone.timedelta(days=1):
        return str(int(diff.total_seconds() / 3600)) + "h"
    elif diff < timezone.timedelta(days=7):
        return str(int(diff.total_seconds() / 86400)) + "d"
    elif diff < timezone.timedelta(days=30):
        return str(int(diff.total_seconds() / 604800)) + "w"
    elif diff < timezone.timedelta(days=365):
        return str(int(diff.total_seconds() / 2592000)) + "M"
    else:
        return str(int(diff.total_seconds() / 31536000)) + "y"


register.filter("custom_timesince", custom_timesince)
