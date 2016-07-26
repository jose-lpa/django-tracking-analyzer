import django

# Major changes in DB lookup transforms between Django 1.9 and Django 1.10.
if django.VERSION < (1, 10):
    from django.db.models.lookups import (
        DateTimeDateTransform,
        HourTransform,
        MinuteTransform
    )
else:
    from django.db.models.functions import (
        TruncDate as DateTimeDateTransform,
        TruncHour as HourTransform,
        TruncMinute as MinuteTransform
    )
