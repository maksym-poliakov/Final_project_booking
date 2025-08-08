from datetime import timedelta
from django.utils import timezone


def get_start_date():
    return timezone.now().date() - timedelta(days=1)