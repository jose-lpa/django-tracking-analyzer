from django.db.models import Count
from django.db.models.functions import TruncDate, Extract


def get_requests_count(queryset):
    """
    This function returns a list of dictionaries containing each one the
    requests count per minute of a certain ``Tracker``s queryset.

    :param queryset: A Django QuerySet of ``Tracker``s.
    :return: List of dictionaries with the requests count per minute.
    """
    return queryset.annotate(
        date=TruncDate('timestamp'),
        hour=Extract('timestamp', 'hour'),
        minute=Extract('timestamp', 'minute')
    ).values(
        'date', 'hour', 'minute'
    ).annotate(requests=Count('pk'))
