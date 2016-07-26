from datetime import date

from django.test import TestCase
from django.utils import timezone

from tracking_analyzer.compat import get_requests_count
from tracking_analyzer.models import Tracker
from .factories import TrackerFactory


class CompatTestCase(TestCase):
    def test_get_requests_count(self):
        """
        The ``get_requests_count`` function must return the same value, despite
        the Django version we are using.
        """
        # Create some `Tracker`s.
        tracker_1 = TrackerFactory.create()
        tracker_2 = TrackerFactory.create()
        tracker_3 = TrackerFactory.create()
        tracker_4 = TrackerFactory.create()
        tracker_5 = TrackerFactory.create()

        # Now assign discrete `timestamp` values.
        tracker_1.timestamp = timezone.datetime(2016, 7, 26, 23, 0)
        tracker_1.save()
        tracker_2.timestamp = timezone.datetime(2016, 7, 26, 23, 0)
        tracker_2.save()
        tracker_3.timestamp = timezone.datetime(2016, 7, 26, 23, 10)
        tracker_3.save()
        tracker_4.timestamp = timezone.datetime(2016, 7, 26, 23, 10)
        tracker_4.save()
        tracker_5.timestamp = timezone.datetime(2016, 7, 26, 23, 10)
        tracker_5.save()

        results = get_requests_count(Tracker.objects.all())

        # Results must always be the same:
        self.assertEqual(
            results[1],
            {
                'date': date(2016, 7, 26),
                'minute': 10,
                'hour': 23,
                'requests': 3
            }
        )
        self.assertEqual(
            results[0],
            {
                'date': date(2016, 7, 26),
                'minute': 0,
                'hour': 23,
                'requests': 2
            }
        )
