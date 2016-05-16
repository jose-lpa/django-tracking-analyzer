from django.contrib.auth.models import User
from django.test import TestCase

from tracking_analyzer.models import Tracker
from .models import Post
from .utils import build_mock_request


class TrackerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='test_user',
            first_name='Test',
            last_name='User',
            email='test_user@maykinmedia.nl'
        )

        self.post = Post.objects.create(
            user=self.user,
            title='Testing post',
            body='This is just a testing post.'
        )

        self.request = build_mock_request('/testing/')

    def test_create_from_request_manager(self):
        """
        Tests the ``create_from_request`` method from the custom
        ``TrackerManager`` in a successful execution.
        """
        tracker = Tracker.objects.create_from_request(self.request, self.post)

        self.assertEqual(tracker.browser, 'Chrome')
        self.assertEqual(tracker.browser_version, '49.0.2623')
        self.assertDictEqual(tracker.cookies, self.request.COOKIES)
        self.assertEqual(tracker.device, 'Other')
        self.assertEqual(tracker.device_type, Tracker.PC)
        self.assertEqual(tracker.system, 'Mac OS X')
        self.assertEqual(tracker.system_version, '10.10.5')
        self.assertEqual(tracker.ip_address, '208.67.222.222')
        self.assertEqual(tracker.ip_country, 'US')
        self.assertEqual(tracker.ip_region, 'CA')
        self.assertEqual(tracker.ip_city, 'San Francisco')
        self.assertEqual(tracker.object_id, self.post.pk)
        self.assertEqual(tracker.user, self.request.user)

    def test_create_from_request_manager_wrong_request(self):
        """
        Tests sanity checks for ``HTTPRequest`` object in the custom manager
        method.
        """
        self.assertRaisesMessage(
            AssertionError,
            '`request` object is not an `HTTPRequest`',
            Tracker.objects.create_from_request,
            'NOT_A_REQUEST', self.post
        )

    def test_create_from_request_manager_wrong_link(self):
        """
        Tests sanity checks for a ``models.Model`` object in the custom
        manager method.
        """
        self.assertRaisesMessage(
            AssertionError,
            '`content_object` is not a Django model',
            Tracker.objects.create_from_request,
            self.request, 'NOT_A_MODEL'
        )

    def test_create_from_request_missing_geoip_data(self):
        """
        If GeoIP data is not available, or the ``geolite2`` function fails, the
        system must keep moving. Just GeoIP data won't be available.
        """
        # Modify the request object to unset the `REMOTE_ADDR` IP meta data.
        # That should make the using of `geoip2.lookup` method technically
        # raise a `ValueError` exception. The system must be smart enough to
        # deal with it.
        self.request.META['REMOTE_ADDR'] = ''

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        # Now check the results. Empty data for IP address and GeoIP stuff.
        self.assertEqual(tracker.ip_address, '')
        self.assertEqual(tracker.ip_country, '')
        self.assertEqual(tracker.ip_region, '')
        self.assertEqual(tracker.ip_city, '')
