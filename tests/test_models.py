import unittest.mock as mock

from django.contrib.auth.models import User
from django.contrib.gis.geoip2 import GeoIP2Exception
from django.test import TestCase

from geoip2.errors import GeoIP2Error

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

    @mock.patch('tracking_analyzer.manager.GeoIP2')
    def test_create_from_request_manager(self, mock_geoip2):
        """
        Tests the ``create_from_request`` method from the custom
        ``TrackerManager`` in a successful execution.
        """
        # Mock the response from `GeoIP2.city()` method.
        mock_geoip2().city.return_value = {
            'country_code': 'US',
            'region': 'CA',
            'city': 'San Francisco'
        }

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        self.assertEqual(tracker.browser, 'Chrome')
        self.assertEqual(tracker.browser_version, '49.0.2623')
        self.assertEqual(tracker.device, 'Mac')
        self.assertEqual(tracker.device_type, Tracker.PC)
        self.assertEqual(tracker.system, 'Mac OS X')
        self.assertEqual(tracker.system_version, '10.10.5')
        self.assertEqual(tracker.ip_address, '208.67.222.222')
        self.assertEqual(tracker.ip_country, 'US')
        self.assertEqual(tracker.ip_region, 'CA')
        self.assertEqual(tracker.ip_city, 'San Francisco')
        self.assertEqual(tracker.object_id, self.post.pk)
        self.assertEqual(tracker.user, self.request.user)

    @mock.patch('tracking_analyzer.manager.GeoIP2')
    def test_create_from_request_manager_null_data(self, mock_geoip2):
        """
        Tests the ``create_from_request`` method from the custom
        ``TrackerManager`` when geo-location data is ``None``.
        """
        # Mock the response from `GeoIP2.city()` method.
        mock_geoip2().city.return_value = {
            'country_code': None,
            'region': None,
            'city': None
        }

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        self.assertEqual(tracker.browser, 'Chrome')
        self.assertEqual(tracker.browser_version, '49.0.2623')
        self.assertEqual(tracker.device, 'Mac')
        self.assertEqual(tracker.device_type, Tracker.PC)
        self.assertEqual(tracker.system, 'Mac OS X')
        self.assertEqual(tracker.system_version, '10.10.5')
        self.assertEqual(tracker.ip_address, '208.67.222.222')
        self.assertEqual(tracker.ip_country, '')
        self.assertEqual(tracker.ip_region, '')
        self.assertEqual(tracker.ip_city, '')
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

    @mock.patch('tracking_analyzer.manager.GeoIP2')
    def test_create_from_request_missing_geoip_data(self, mock_geoip2):
        """
        If GeoIP data is not available, or the ``GeoIP2.city`` function fails,
        the system must keep moving. Just GeoIP data won't be available.
        """
        # Modify the request object to unset the `REMOTE_ADDR` IP meta data.
        # That should make the using of `ipware.ip.get_client_ip()` method
        # return an empty IP value. The system must deal with empty IP
        # addresses.
        self.request.META['REMOTE_ADDR'] = ''

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        # Now check the results. Empty data for IP address and GeoIP stuff.
        self.assertEqual(tracker.ip_address, None)
        self.assertEqual(tracker.ip_country, '')
        self.assertEqual(tracker.ip_region, '')
        self.assertEqual(tracker.ip_city, '')

        # And `GeoIP2` should have been never called.
        self.assertFalse(mock_geoip2().city.called)

    @mock.patch('tracking_analyzer.manager.GeoIP2')
    def test_create_from_request_django_geoip_exception(self, mock_geoip2):
        """
        Tests Django ``contrib.gis.geoip2.GeoIP2Exception`` handling.
        """
        mock_geoip2().city.side_effect = GeoIP2Exception

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        # Now check the results. Empty data for IP address and GeoIP stuff.
        self.assertEqual(tracker.ip_address, '208.67.222.222')
        self.assertEqual(tracker.ip_country, '')
        self.assertEqual(tracker.ip_region, '')
        self.assertEqual(tracker.ip_city, '')

    @mock.patch('tracking_analyzer.manager.GeoIP2')
    def test_create_from_request_geoip2_exception(self, mock_geoip2):
        """
        Tests Django ``geoip2.GeoIP2Error`` handling.
        """
        mock_geoip2().city.side_effect = GeoIP2Error

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        # Now check the results. Empty data for IP address and GeoIP stuff.
        self.assertEqual(tracker.ip_address, '208.67.222.222')
        self.assertEqual(tracker.ip_country, '')
        self.assertEqual(tracker.ip_region, '')
        self.assertEqual(tracker.ip_city, '')

    @mock.patch('tracking_analyzer.manager.GeoIP2')
    @mock.patch(
        'user_agents.parsers.UserAgent.is_pc', new_callable=mock.PropertyMock)
    def test_create_from_request_is_pc(self, agent_mock, geoip2_mock):
        """
        Tests the ``create_from_request`` method when the requesting device is
        a PC.
        """
        # Mock the response from `GeoIP2.city()` method.
        geoip2_mock().city.return_value = {
            'country_code': None,
            'region': None,
            'city': None
        }
        agent_mock.return_value = True

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        self.assertEqual(tracker.device_type, Tracker.PC)

    @mock.patch('tracking_analyzer.manager.GeoIP2')
    @mock.patch(
        'user_agents.parsers.UserAgent.is_mobile',
        new_callable=mock.PropertyMock)
    def test_create_from_request_is_mobile(self, agent_mock, geoip2_mock):
        """
        Tests the ``create_from_request`` method when the requesting device is
        a mobile device.
        """
        # Mock the response from `GeoIP2.city()` method.
        geoip2_mock().city.return_value = {
            'country_code': None,
            'region': None,
            'city': None
        }
        agent_mock.return_value = True

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        self.assertEqual(tracker.device_type, Tracker.MOBILE)

    @mock.patch('tracking_analyzer.manager.GeoIP2')
    @mock.patch(
        'user_agents.parsers.UserAgent.is_tablet',
        new_callable=mock.PropertyMock)
    def test_create_from_request_is_tablet(self, agent_mock, geoip2_mock):
        """
        Tests the ``create_from_request`` method when the requesting device is
        a tablet device.
        """
        # Mock the response from `GeoIP2.city()` method.
        geoip2_mock().city.return_value = {
            'country_code': None,
            'region': None,
            'city': None
        }
        agent_mock.return_value = True

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        self.assertEqual(tracker.device_type, Tracker.TABLET)

    @mock.patch('tracking_analyzer.manager.GeoIP2')
    @mock.patch(
        'user_agents.parsers.UserAgent.is_pc', new_callable=mock.PropertyMock)
    @mock.patch(
        'user_agents.parsers.UserAgent.is_bot', new_callable=mock.PropertyMock)
    def test_create_from_request_is_bot(self, bot_mock, pc_mock, geoip2_mock):
        """
        Tests the ``create_from_request`` method when the requesting device is
        a spider bot.
        """
        # Mock the response from `GeoIP2.city()` method.
        geoip2_mock().city.return_value = {
            'country_code': None,
            'region': None,
            'city': None
        }
        bot_mock.return_value = True
        pc_mock.return_value = False

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        self.assertEqual(tracker.device_type, Tracker.BOT)

    @mock.patch('tracking_analyzer.manager.GeoIP2')
    @mock.patch(
        'user_agents.parsers.UserAgent.is_pc', new_callable=mock.PropertyMock)
    @mock.patch(
        'user_agents.parsers.UserAgent.is_mobile',
        new_callable=mock.PropertyMock)
    @mock.patch(
        'user_agents.parsers.UserAgent.is_tablet',
        new_callable=mock.PropertyMock)
    @mock.patch(
        'user_agents.parsers.UserAgent.is_bot', new_callable=mock.PropertyMock)
    def test_create_from_request_is_unknown(
        self, bot_mock, tablet_mock, mobile_mock, pc_mock, geoip2_mock
    ):
        """
        Tests the ``create_from_request`` method when the requesting device is
        an unknown device.
        """
        # Mock the response from `GeoIP2.city()` method.
        geoip2_mock().city.return_value = {
            'country_code': None,
            'region': None,
            'city': None
        }

        bot_mock.return_value = False
        tablet_mock.return_value = False
        mobile_mock.return_value = False
        pc_mock.return_value = False

        tracker = Tracker.objects.create_from_request(self.request, self.post)

        self.assertEqual(tracker.device_type, Tracker.UNKNOWN)

    @mock.patch('tracking_analyzer.manager.GeoIP2')
    def test_create_from_request_wrong_user_agent(self, mock_geoip2):
        """
        Tests the ``create_from_request`` method with a wrong user agent.
        """
        # Mock the response from `GeoIP2.city()` method.
        mock_geoip2().city.return_value = {
            'country_code': 'US',
            'region': 'CA',
            'city': 'San Francisco'
        }

        request = build_mock_request(
            '/testing/', 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxbot'
        )

        tracker = Tracker.objects.create_from_request(request, self.post)

        self.assertEqual(tracker.browser, 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        self.assertEqual(tracker.browser_version, '')
        self.assertEqual(tracker.device, 'Spider')
        self.assertEqual(tracker.device_type, Tracker.BOT)
        self.assertEqual(tracker.system, 'Other')
        self.assertEqual(tracker.system_version, '')
        self.assertEqual(tracker.ip_address, '208.67.222.222')
        self.assertEqual(tracker.ip_country, 'US')
        self.assertEqual(tracker.ip_region, 'CA')
        self.assertEqual(tracker.ip_city, 'San Francisco')
        self.assertEqual(tracker.object_id, self.post.pk)
        self.assertEqual(tracker.user, self.request.user)
