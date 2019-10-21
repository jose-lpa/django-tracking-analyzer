import json

from django.contrib.admin import AdminSite
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from django_countries import countries

from tracking_analyzer.admin import TrackerAdmin
from tracking_analyzer.models import Tracker
from .factories import TrackerFactory, UserFactory


class TrackerAdminTestCase(TestCase):
    def setUp(self):
        self.tracker_1 = TrackerFactory.create(
            device_type=Tracker.PC, ip_country='ESP')
        self.tracker_2 = TrackerFactory.create(
            device_type=Tracker.MOBILE, ip_country='NLD')
        self.tracker_3 = TrackerFactory.create(
            device_type=Tracker.TABLET, ip_country='GBR')

        self.admin_site = AdminSite(name='tracker_admin')
        self.tracker_admin = TrackerAdmin(Tracker, self.admin_site)

        self.url = reverse('admin:tracking_analyzer_tracker_changelist')

        # Create a superuser and mock a request made by it.
        self.user = UserFactory.create(is_staff=True, is_superuser=True)
        self.request = RequestFactory().get('/')
        self.request.user = self.user

    def test_content_object_link(self):
        """
        Test response of the ``TrackerAdmin.content_object_link`` method.
        """
        response = self.tracker_admin.content_object_link(self.tracker_1)

        self.assertEqual(
            response,
            '<a href="{0}?content_type__id__exact={1}&object_id__exact={2}">'
            '{3}</a>'.format(
                reverse('admin:tracking_analyzer_tracker_changelist'),
                self.tracker_1.content_type.id,
                self.tracker_1.object_id,
                self.tracker_1
            )
        )

    def test_ip_address_link(self):
        """
        Test response of the ``TrackerAdmin.ip_address_link`` method when
        an IP address is available.
        """
        response = self.tracker_admin.ip_address_link(self.tracker_1)

        self.assertEqual(
            response,
            '<a href="{0}?ip_address__exact={1}">{1}</a>'.format(
                reverse('admin:tracking_analyzer_tracker_changelist'),
                self.tracker_1.ip_address,
            )
        )

    def test_ip_address_link_no_address(self):
        """
        Test response of the ``TrackerAdmin.ip_address_link`` method when
        an IP address is NOT available.
        """
        self.tracker_1.ip_address = None
        self.tracker_1.save()

        response = self.tracker_admin.ip_address_link(self.tracker_1)

        self.assertEqual(response, '-')

    def test_ip_country_link(self):
        """
        Test response of the ``TrackerAdmin.ip_country_link`` method when
        Country data is available.
        """
        response = self.tracker_admin.ip_country_link(self.tracker_1)

        self.assertEqual(
            response,
            '<a href="{0}?ip_country__exact={1}">{2}</a>'.format(
                reverse('admin:tracking_analyzer_tracker_changelist'),
                self.tracker_1.ip_country,
                self.tracker_1.ip_country.name
            )
        )

    def test_ip_country_link_no_country(self):
        """
        Test response of the ``TrackerAdmin.ip_country_link`` method when
        Country data is NOT available.
        """
        self.tracker_1.ip_country = ''
        self.tracker_1.save()

        response = self.tracker_admin.ip_country_link(self.tracker_1)

        self.assertEqual(response, '-')

    def test_ip_city_link(self):
        """
        Test response of the ``TrackerAdmin.ip_city_link`` method when City
        data is available.
        """
        response = self.tracker_admin.ip_city_link(self.tracker_1)

        self.assertEqual(
            response,
            '<a href="{0}?ip_city__exact={1}">{1}</a>'.format(
                reverse('admin:tracking_analyzer_tracker_changelist'),
                self.tracker_1.ip_city,
            )
        )

    def test_ip_city_link_no_city(self):
        """
        Test response of the ``TrackerAdmin.ip_city_link`` method when City
        data is NOT available.
        """
        self.tracker_1.ip_city = ''
        self.tracker_1.save()

        response = self.tracker_admin.ip_city_link(self.tracker_1)

        self.assertEqual(response, '-')

    def test_user_link(self):
        """
        Test response of the ``TrackerAdmin.user_link`` method when User data
        is available.
        """
        response = self.tracker_admin.user_link(self.tracker_1)

        self.assertEqual(
            response,
            '<a href="{0}?user__id__exact={1}">{2}</a>'.format(
                reverse('admin:tracking_analyzer_tracker_changelist'),
                self.tracker_1.user.pk,
                self.tracker_1.user
            )
        )

    def test_user_link_no_user(self):
        """
        Test response of the ``TrackerAdmin.user_link`` method when User data
        is NOT available.
        """
        self.tracker_1.user = None
        self.tracker_1.save()

        response = self.tracker_admin.user_link(self.tracker_1)

        self.assertEqual(response, 'Anonymous')

    def test_has_add_permission_always_false(self):
        """
        The ``has_add_permission`` method must always return ``False``, because
        trackers should not be manually created by users.
        """
        self.assertFalse(self.tracker_admin.has_add_permission(self.request))

    def test_change_view_overridden_to_dismiss_edition_buttons(self):
        response = self.tracker_admin.change_view(
            self.request, str(self.tracker_1.pk))

        self.assertFalse(response.context_data['show_save_and_add_another'])
        self.assertFalse(response.context_data['show_save_and_continue'])
        self.assertFalse(response.context_data['show_save'])

    def test_changelist_view_context_countries_count_present(self):
        """
        The ``get_request_count`` context contains a dataset for countries
        requests when not filtering by country.
        """
        url = reverse('admin:tracking_analyzer_tracker_changelist')
        request = RequestFactory().get(url)
        request.user = self.user

        response = self.tracker_admin.changelist_view(request)
        self.assertEqual(
            response.context_data['countries_count'],
            '[["{0}", 1], ["{1}", 1], ["{2}", 1]]'.format(
                countries.alpha3(self.tracker_1.ip_country),
                countries.alpha3(self.tracker_3.ip_country),
                countries.alpha3(self.tracker_2.ip_country),
            )
        )

    def test_changelist_view_context_countries_count_not_present(self):
        """
        The ``get_request_count`` context should NOT contain a dataset for
        countries requests when user is filtering by country.
        """
        url = '{0}?ip_country__exact=ES'.format(
            reverse('admin:tracking_analyzer_tracker_changelist'))
        request = RequestFactory().get(url)
        request.user = self.user

        response = self.tracker_admin.changelist_view(request)
        self.assertNotIn('countries_count', response.context_data)

    def test_changelist_view_context_devices_count_present(self):
        """
        The ``get_request_count`` context contains a dataset for device types
        when user is not filtering by them.
        """
        url = reverse('admin:tracking_analyzer_tracker_changelist')
        request = RequestFactory().get(url)
        request.user = self.user

        response = self.tracker_admin.changelist_view(request)
        data = json.loads(response.context_data['devices_count'])

        self.assertEqual(len(data), 3)
        self.assertIn(
            {
                "count": 1,
                "device_type": self.tracker_1.device_type,
            },
            data
        )
        self.assertIn(
            {
                "count": 1,
                "device_type": self.tracker_2.device_type,
            },
            data
        )
        self.assertIn(
            {
                "count": 1,
                "device_type": self.tracker_3.device_type,
            },
            data
        )

    def test_changelist_view_context_devices_count_not_present(self):
        """
        The ``get_request_count`` context should NOT contain a dataset for
        device types when user is filtering by them.
        """
        url = '{0}?device_type__exact=pc'.format(
            reverse('admin:tracking_analyzer_tracker_changelist'))
        request = RequestFactory().get(url)
        request.user = self.user

        response = self.tracker_admin.changelist_view(request)
        self.assertNotIn('devices_count', response.context_data)

    def test_changelist_view_requests_count(self):
        """
        The ``get_request_count`` context must always contain a dataset for
        requests-per-minute count.
        """
        # Now assign discrete `timestamp` values.
        self.tracker_1.timestamp = timezone.datetime(2016, 7, 26, 23, 0)
        self.tracker_1.save()
        self.tracker_2.timestamp = timezone.datetime(2016, 7, 26, 23, 0)
        self.tracker_2.save()
        self.tracker_3.timestamp = timezone.datetime(2016, 7, 26, 23, 10)
        self.tracker_3.save()

        url = reverse('admin:tracking_analyzer_tracker_changelist')
        request = RequestFactory().get(url)
        request.user = self.user

        response = self.tracker_admin.changelist_view(request)
        data = json.loads(response.context_data['requests_count'])

        self.assertEqual(len(data), 2)
        self.assertIn(
            {
                "date": self.tracker_1.timestamp.strftime('%Y-%m-%dT%H:%M'),
                "requests": 2
            },
            data
        )
        self.assertIn(
            {
                "date": self.tracker_3.timestamp.strftime('%Y-%m-%dT%H:%M'),
                "requests": 1
            },
            data
        )

    def test_changelist_post_delete(self):
        """
        Tests that the 'changelist' POST action stills working.
        """
        self.client.login(username=self.user.username, password='testing')
        response = self.client.post(
            self.url,
            data={
                '_selected_action': str(self.tracker_1.pk),
                'action': 'delete_selected'  # Add 'post': 'yes' later.
            }
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            self.url,
            data={
                '_selected_action': str(self.tracker_1.pk),
                'action': 'delete_selected',
                'post': 'yes'
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)

        # `self.tracker_1` was actually deleted.
        self.assertFalse(Tracker.objects.filter(pk=self.tracker_1.pk).exists())
