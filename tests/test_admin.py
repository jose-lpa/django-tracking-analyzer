from django.contrib.admin import AdminSite
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from tracking_analyzer.admin import TrackerAdmin
from .factories import TrackerFactory, UserFactory
from .models import Post


class TrackerAdminTestCase(TestCase):
    def setUp(self):
        self.tracker = TrackerFactory.create()

        self.admin_site = AdminSite(name='tracker_admin')
        self.tracker_admin = TrackerAdmin(Post, self.admin_site)

        # Create a superuser and mock a request made by it.
        self.user = UserFactory.create(is_staff=True, is_superuser=True)
        self.request = RequestFactory().get('/')
        self.request.user = self.user

    def test_content_object_link(self):
        """
        Test response of the ``TrackerAdmin.content_object_link`` method.
        """
        response = self.tracker_admin.content_object_link(self.tracker)

        self.assertEqual(
            response,
            '<a href="{0}?content_type__id__exact={1}&object_id__exact={2}">'
            '{3}</a>'.format(
                reverse('admin:tracking_analyzer_tracker_changelist'),
                self.tracker.content_type.id,
                self.tracker.object_id,
                self.tracker
            )
        )

    def test_ip_address_link(self):
        """
        Test response of the ``TrackerAdmin.ip_address_link`` method when
        an IP address is available.
        """
        response = self.tracker_admin.ip_address_link(self.tracker)

        self.assertEqual(
            response,
            '<a href="{0}?ip_address__exact={1}">{1}</a>'.format(
                reverse('admin:tracking_analyzer_tracker_changelist'),
                self.tracker.ip_address,
            )
        )

    def test_ip_address_link_no_address(self):
        """
        Test response of the ``TrackerAdmin.ip_address_link`` method when
        an IP address is NOT available.
        """
        self.tracker.ip_address = None
        self.tracker.save()

        response = self.tracker_admin.ip_address_link(self.tracker)

        self.assertEqual(response, '-')

    def test_ip_country_link(self):
        """
        Test response of the ``TrackerAdmin.ip_country_link`` method when
        Country data is available.
        """
        response = self.tracker_admin.ip_country_link(self.tracker)

        self.assertEqual(
            response,
            '<a href="{0}?ip_country__exact={1}">{2}</a>'.format(
                reverse('admin:tracking_analyzer_tracker_changelist'),
                self.tracker.ip_country,
                self.tracker.ip_country.name
            )
        )

    def test_ip_country_link_no_country(self):
        """
        Test response of the ``TrackerAdmin.ip_country_link`` method when
        Country data is NOT available.
        """
        self.tracker.ip_country = ''
        self.tracker.save()

        response = self.tracker_admin.ip_country_link(self.tracker)

        self.assertEqual(response, '-')

    def test_ip_city_link(self):
        """
        Test response of the ``TrackerAdmin.ip_city_link`` method when City
        data is available.
        """
        response = self.tracker_admin.ip_city_link(self.tracker)

        self.assertEqual(
            response,
            '<a href="{0}?ip_city__exact={1}">{1}</a>'.format(
                reverse('admin:tracking_analyzer_tracker_changelist'),
                self.tracker.ip_city,
            )
        )

    def test_ip_city_link_no_city(self):
        """
        Test response of the ``TrackerAdmin.ip_city_link`` method when City
        data is NOT available.
        """
        self.tracker.ip_city = ''
        self.tracker.save()

        response = self.tracker_admin.ip_city_link(self.tracker)

        self.assertEqual(response, '-')

    def test_user_link(self):
        """
        Test response of the ``TrackerAdmin.user_link`` method when User data
        is available.
        """
        response = self.tracker_admin.user_link(self.tracker)

        self.assertEqual(
            response,
            '<a href="{0}?user__id__exact={1}">{2}</a>'.format(
                reverse('admin:tracking_analyzer_tracker_changelist'),
                self.tracker.user.pk,
                self.tracker.user
            )
        )

    def test_user_link_no_user(self):
        """
        Test response of the ``TrackerAdmin.user_link`` method when User data
        is NOT available.
        """
        self.tracker.user = None
        self.tracker.save()

        response = self.tracker_admin.user_link(self.tracker)

        self.assertEqual(response, 'Anonymous')

    def test_has_add_permission_always_false(self):
        """
        The ``has_add_permission`` method must always return ``False``, because
        trackers should not be manually created by users.
        """
        self.assertFalse(self.tracker_admin.has_add_permission(self.request))

    def test_change_view_overridden_to_dismiss_edition_buttons(self):
        response = self.tracker_admin.change_view(self.request, str(self.tracker.pk))

        self.assertFalse(response.context_data['show_save_and_add_another'])
        self.assertFalse(response.context_data['show_save_and_continue'])
        self.assertFalse(response.context_data['show_save'])
