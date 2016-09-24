import os

from django.conf import settings
from django.core.management import call_command, CommandError
from django.test import override_settings, TestCase

from tracking_analyzer.compat import HTTPError, mock, URLError


class InstallGeoIPDatasetTestCase(TestCase):
    @override_settings(GEOIP_PATH=None)
    def test_handle_missing_geoip_path(self):
        """
        The project settings have to have a ``GEOIP_PATH``.
        """
        del settings.GEOIP_PATH

        self.assertRaisesMessage(
            CommandError,
            '`GEOIP_PATH` setting not present. Unable to get the GeoIP '
            'dataset.',
            call_command, 'install_geoip_dataset'
        )

    @override_settings(TRACKING_ANALYZER_MAXMIND_URL=None)
    def test_handle_no_url_arg_no_url_setting(self):
        """
        If the user doesn't provide a base URL to download the dataset from, at
        least the ``TRACKING_ANALYZER_MAXMIND_URL`` setting have to be present.
        """
        del settings.TRACKING_ANALYZER_MAXMIND_URL

        self.assertRaisesMessage(
            CommandError,
            '`TRACKING_ANALYZER_MAXMIND_URL` setting not present. Unable to '
            'get the GeoIP dataset.',
            call_command, 'install_geoip_dataset'
        )

    @override_settings(TRACKING_ANALYZER_MAXMIND_COUNTRIES=None)
    def test_handle_no_dataset_arg_no_countries_setting(self):
        """
        If the user doesn't provide a dataset file name to be downloaded, at
        least the ``TRACKING_ANALYZER_MAXMIND_COUNTRIES`` setting have to be
        present.
        """
        del settings.TRACKING_ANALYZER_MAXMIND_COUNTRIES

        self.assertRaisesMessage(
            CommandError,
            '`TRACKING_ANALYZER_MAXMIND_COUNTRIES` setting not present. Unable'
            ' to get the GeoIP dataset.',
            call_command, 'install_geoip_dataset'
        )

    @override_settings(TRACKING_ANALYZER_MAXMIND_URL=None)
    @mock.patch('tracking_analyzer.management.commands.install_geoip_dataset.Command.install_dataset')
    def test_handle_no_url_setting_manual_target(self, install_mock):
        """
        If the base URL is not available, the user should still be able to
        specify it in in the command arguments.
        """
        del settings.TRACKING_ANALYZER_MAXMIND_URL

        call_command('install_geoip_dataset', url='http://www.maykinmedia.nl')

        calls = [
            mock.call(
                settings.GEOIP_PATH,
                mm_url='http://www.maykinmedia.nl',
                mm_dataset=settings.TRACKING_ANALYZER_MAXMIND_COUNTRIES
            ),
            mock.call(
                settings.GEOIP_PATH,
                mm_url='http://www.maykinmedia.nl',
                mm_dataset=settings.TRACKING_ANALYZER_MAXMIND_CITIES
            )
        ]

        install_mock.assert_has_calls(calls)

    @override_settings(TRACKING_ANALYZER_MAXMIND_COUNTRIES=None)
    @mock.patch('tracking_analyzer.management.commands.install_geoip_dataset.Command.install_dataset')
    def test_handle_no_countries_setting_manual_target(self, install_mock):
        """
        If the countries file name is not available, the user should still be
        able to specify it in in the command arguments.
        """
        del settings.TRACKING_ANALYZER_MAXMIND_COUNTRIES

        call_command('install_geoip_dataset', countries='countries_db.mmdb')

        calls = [
            mock.call(
                settings.GEOIP_PATH,
                mm_url=settings.TRACKING_ANALYZER_MAXMIND_URL,
                mm_dataset='countries_db.mmdb'
            ),
            mock.call(
                settings.GEOIP_PATH,
                mm_url=settings.TRACKING_ANALYZER_MAXMIND_URL,
                mm_dataset=settings.TRACKING_ANALYZER_MAXMIND_CITIES
            )
        ]

        install_mock.assert_has_calls(calls)

    @override_settings(TRACKING_ANALYZER_MAXMIND_CITIES=None)
    @mock.patch('tracking_analyzer.management.commands.install_geoip_dataset.Command.install_dataset')
    def test_a_handle_no_cities_setting_manual_target(self, install_mock):
        """
        If the cities file name is not available, the user should still be
        able to specify it in in the command arguments.
        """
        del settings.TRACKING_ANALYZER_MAXMIND_CITIES

        call_command('install_geoip_dataset', cities='cities_db.mmdb')

        calls = [
            mock.call(
                settings.GEOIP_PATH,
                mm_url=settings.TRACKING_ANALYZER_MAXMIND_URL,
                mm_dataset=settings.TRACKING_ANALYZER_MAXMIND_COUNTRIES
            ),
            mock.call(
                settings.GEOIP_PATH,
                mm_url=settings.TRACKING_ANALYZER_MAXMIND_URL,
                mm_dataset='cities_db.mmdb'
            )
        ]

        install_mock.assert_has_calls(calls)

    @mock.patch('tracking_analyzer.management.commands.install_geoip_dataset.Command.install_dataset')
    def test_handle_straight_run_no_user_input_needed(self, install_mock):
        """
        Test the management command in a straight situation where the system
        does not have any dataset installed yet and the settings are okay.
        """
        call_command('install_geoip_dataset')

        calls = [
            mock.call(
                settings.GEOIP_PATH,
                mm_url=settings.TRACKING_ANALYZER_MAXMIND_URL,
                mm_dataset=settings.TRACKING_ANALYZER_MAXMIND_COUNTRIES
            ),
            mock.call(
                settings.GEOIP_PATH,
                mm_url=settings.TRACKING_ANALYZER_MAXMIND_URL,
                mm_dataset=settings.TRACKING_ANALYZER_MAXMIND_CITIES
            )
        ]

        install_mock.assert_has_calls(calls)

    @mock.patch('os.path.isfile')
    @mock.patch('tracking_analyzer.management.commands.install_geoip_dataset.Command.user_input')
    @mock.patch('tracking_analyzer.management.commands.install_geoip_dataset.Command.install_dataset')
    def test_handle_existing_datasets_user_action_required_no(self, mock_command, mock_input, mock_isfile):
        """
        Test the command running in a situation where there is an existent
        dataset already installed and the user responds "NO" when asked to
        update it.
        """
        mock_isfile.return_value = True  # A dataset is already placed.
        mock_input.return_value = False  # User said 'no'

        call_command('install_geoip_dataset')

        self.assertFalse(mock_command.called)

    @mock.patch('os.path.isfile')
    @mock.patch('tracking_analyzer.management.commands.install_geoip_dataset.Command.user_input')
    @mock.patch('tracking_analyzer.management.commands.install_geoip_dataset.Command.install_dataset')
    def test_handle_existing_countries_user_action_required_yes(self, mock_command, mock_input, mock_isfile):
        """
        Test the command running in a situation where there is an existent
        dataset already installed and the user responds "YES" when asked to
        update it.
        """
        mock_isfile.return_value = True  # A dataset is already placed.
        mock_input.return_value = True   # User said 'yes'

        call_command('install_geoip_dataset')

        calls = [
            mock.call(
                settings.GEOIP_PATH,
                mm_url=settings.TRACKING_ANALYZER_MAXMIND_URL,
                mm_dataset=settings.TRACKING_ANALYZER_MAXMIND_COUNTRIES
            ),
            mock.call(
                settings.GEOIP_PATH,
                mm_url=settings.TRACKING_ANALYZER_MAXMIND_URL,
                mm_dataset=settings.TRACKING_ANALYZER_MAXMIND_CITIES
            )
        ]

        mock_command.assert_has_calls(calls)

    @mock.patch('tracking_analyzer.management.commands.install_geoip_dataset.urlopen')
    def test_install_dataset_urlopen_http_error(self, urlopen_mock):
        """
        ``install_dataset`` method is able to handle ``HTTPError`` exceptions.
        """
        urlopen_mock.side_effect = HTTPError(
            url='http://www.maykinmedia.nl',
            code=403,
            msg='Forbidden',
            hdrs={},
            fp=None
        )

        self.assertRaisesMessage(
            CommandError,
            'Unable to download MaxMind dataset.',
            call_command, 'install_geoip_dataset'
        )

    @mock.patch('tracking_analyzer.management.commands.install_geoip_dataset.urlopen')
    def test_install_dataset_urlopen_url_error(self, urlopen_mock):
        """
        ``install_dataset`` method is able to handle ``URLError`` exceptions.
        """
        urlopen_mock.side_effect = URLError(reason='unknown url type')

        self.assertRaisesMessage(
            CommandError,
            'Unable to download MaxMind dataset.',
            call_command, 'install_geoip_dataset'
        )
