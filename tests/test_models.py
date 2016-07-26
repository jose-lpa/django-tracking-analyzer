from django.contrib.auth.models import User
from django.contrib.gis.geoip2 import GeoIP2Exception
from django.test import TestCase

from geoip2.errors import GeoIP2Error

from tracking_analyzer.compat.mock import patch
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

    @patch('django.contrib.gis.geoip2.GeoIP2.city')
    def test_create_from_request_manager(self, mock):
        """
        Tests the ``create_from_request`` method from the custom
        ``TrackerManager`` in a successful execution.
        """
        # Mock the response from `GeoIP2.city()` method.
        mock.return_value = {
            'country_code': 'US',
            'region': 'CA',
            'city': 'San Francisco'
        }

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        self.assertEqual(tracker.browser, 'Chrome')
        self.assertEqual(tracker.browser_version, '49.0.2623')
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

    @patch('django.contrib.gis.geoip2.GeoIP2.city')
    def test_create_from_request_missing_geoip_data(self, mock):
        """
        If GeoIP data is not available, or the ``GeoIP2.city`` function fails,
        the system must keep moving. Just GeoIP data won't be available.
        """
        # Modify the request object to unset the `REMOTE_ADDR` IP meta data.
        # That should make the using of `ipware.ip.get_real_ip()` method return
        # an empty IP value. The system must deal with empty IP addresses.
        self.request.META['REMOTE_ADDR'] = ''

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        # Now check the results. Empty data for IP address and GeoIP stuff.
        self.assertEqual(tracker.ip_address, '')
        self.assertEqual(tracker.ip_country, '')
        self.assertEqual(tracker.ip_region, '')
        self.assertEqual(tracker.ip_city, '')

        # And `GeoIP2` should have been never called.
        self.assertFalse(mock.called)

    @patch('django.contrib.gis.geoip2.GeoIP2.city')
    def test_create_from_request_django_geoip_exception(self, mock):
        """
        Tests Django ``contrib.gis.geoip2.GeoIP2Exception`` handling.
        """
        mock.side_effect = GeoIP2Exception

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        # Now check the results. Empty data for IP address and GeoIP stuff.
        self.assertEqual(tracker.ip_address, '208.67.222.222')
        self.assertEqual(tracker.ip_country, '')
        self.assertEqual(tracker.ip_region, '')
        self.assertEqual(tracker.ip_city, '')

    @patch('django.contrib.gis.geoip2.GeoIP2.city')
    def test_create_from_request_geoip2_exception(self, mock):
        """
        Tests Django ``geoip2.GeoIP2Error`` handling.
        """
        mock.side_effect = GeoIP2Error

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        # Now check the results. Empty data for IP address and GeoIP stuff.
        self.assertEqual(tracker.ip_address, '208.67.222.222')
        self.assertEqual(tracker.ip_country, '')
        self.assertEqual(tracker.ip_region, '')
        self.assertEqual(tracker.ip_city, '')
