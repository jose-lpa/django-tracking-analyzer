import django
from django.db.models import Count

# Mock facility for unit testing.
try:
    # Python 3
    import unittest.mock as mock
except ImportError:
    # Python 2
    import mock


def get_requests_count(queryset):
    """
    Major changes in DB lookup transforms between Django 1.9 and Django 1.10.

    This function returns a list of dictionaries containing each one the
    requests count per minute of a certain ``Tracker``s queryset.

    :param queryset: A Django QuerySet of ``Tracker``s.
    :return: List of dictionaries with the requests count per minute.
    """
    if django.VERSION < (1, 10):
        from django.db.models.lookups import (
            DateTimeDateTransform, HourTransform, MinuteTransform
        )

        return queryset.annotate(
            date=DateTimeDateTransform('timestamp'),
            hour=HourTransform('timestamp'),
            minute=MinuteTransform('timestamp')
        ).values(
            'date', 'hour', 'minute'
        ).annotate(requests=Count('pk', 'date')).order_by()
    else:
        from django.db.models.functions import TruncDate, Extract

        return queryset.annotate(
            date=TruncDate('timestamp'),
            hour=Extract('timestamp', 'hour'),
            minute=Extract('timestamp', 'minute')
        ).values(
            'date', 'hour', 'minute'
        ).annotate(requests=Count('pk', 'date'))
