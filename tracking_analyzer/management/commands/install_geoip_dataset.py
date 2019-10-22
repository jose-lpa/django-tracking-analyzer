import gzip
from os.path import isfile, join, splitext
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Installs/updates the MaxMind(R) datasets. Plase check ' \
           'https://www.maxmind.com/ for more information.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            help='Base URL where the MaxMind(R) datasets are available.'
                 ' Optional, probably better not to use it.'
        )
        parser.add_argument(
            '--countries',
            help='Remote file name for the MaxMind(R) Country dataset.'
                 ' Optional, probably better not to use it.'
        )
        parser.add_argument(
            '--cities',
            help='Remote file name for the MaxMind(R) City dataset.'
                 ' Optional, probably better not to use it.'
        )

    def user_input(self):
        """
        Helper method to handle user input when required.
        """
        if input('(y/n) ').lower() in ['y', 'yes']:
            return True

        return False

    def install_dataset(self, geoip_dir, mm_url, mm_dataset):
        """
        Downloads the MaxMind datasets and unpacks it into the selected Django
        project ``GEOIP_PATH`` directory.

        :param geoip_dir: The directory where the GeoIP datasets live, set in
        the ``GEOIP_PATH`` Django project setting.
        :param mm_url: The URL where the dataset has to be retrieved from.
        :param mm_dataset: The name of the dataset file.
        """
        url = '{0}{1}'.format(mm_url, mm_dataset)

        try:
            resource = urlopen(url)
        except (HTTPError, URLError) as error:
            self.stderr.write(str(error))
            raise CommandError('Unable to download MaxMind dataset.')

        filename = join(geoip_dir, mm_dataset)

        with open(filename, 'wb') as file:
            metadata = resource.info()
            if hasattr(metadata, 'getheaders'):
                meta_func = metadata.getheaders
            else:
                meta_func = metadata.get_all

            meta_length = meta_func('Content-Length')
            file_size = None
            if meta_length:
                file_size = int(meta_length[0])

            print("Downloading: {0} Bytes: {1}".format(url, file_size))

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = resource.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                file.write(buffer)

                status = "{0:16}".format(file_size_dl)
                if file_size:
                    status += " downloaded [{0:6.2f}%]".format(
                        file_size_dl * 100 / file_size)
                status += chr(13)
                print(status, end="")
            print()

        self.stdout.write('Uncompressing downloaded dataset...')

        with gzip.open(filename, 'rb') as gzipped:
            with open(splitext(filename)[0], 'wb') as gunzipped:
                gunzipped.write(gzipped.read())
                self.stdout.write(
                    '{0} dataset installed and ready for use.'.format(
                        splitext(filename)[0]
                    )
                )

    def checkout_datasets(self, geoip_dir, url, datasets):
        for dataset in datasets:
            if isfile(join(geoip_dir, splitext(dataset)[0])):
                self.stdout.write(
                    '\nSeems that MaxMind dataset {0} is already installed in '
                    '"{1}". Do you want to reinstall it?'.format(
                        dataset, geoip_dir)
                )

                if self.user_input() is True:
                    self.stdout.write(
                        'Updating MaxMind {0} dataset...'.format(dataset))
                    self.install_dataset(
                        geoip_dir, mm_url=url, mm_dataset=dataset)
                else:
                    self.stdout.write(
                        '{0} dataset should be ready.'.format(dataset))
            else:
                self.stdout.write(
                    'Installing MaxMind {0} dataset...'.format(dataset))
                self.install_dataset(geoip_dir, mm_url=url, mm_dataset=dataset)

    def handle(self, *args, **options):
        # Check `GEOIP_PATH` setting is ready.
        try:
            geoip_dir = getattr(settings, 'GEOIP_PATH')
        except AttributeError:
            raise CommandError('`GEOIP_PATH` setting not present. Unable to '
                               'get the GeoIP dataset.')

        url = options.get('url')
        if not url:
            # Check `TRACKING_ANALYZER_MAXMIND_URL` setting is ready.
            try:
                url = getattr(settings, 'TRACKING_ANALYZER_MAXMIND_URL')
            except AttributeError:
                raise CommandError(
                    '`TRACKING_ANALYZER_MAXMIND_URL` setting not present. '
                    'Unable to get the GeoIP dataset.'
                )

        countries = options.get('countries')
        if not countries:
            # Check `TRACKING_ANALYZER_MAXMIND_COUNTRIES` setting is ready.
            try:
                countries = getattr(
                    settings, 'TRACKING_ANALYZER_MAXMIND_COUNTRIES')
            except AttributeError:
                raise CommandError(
                    '`TRACKING_ANALYZER_MAXMIND_COUNTRIES` setting not '
                    'present. Unable to get the GeoIP dataset.'
                )

        cities = options.get('cities')
        if not cities:
            # Check `TRACKING_ANALYZER_MAXMIND_CITIES` setting is ready.
            try:
                cities = getattr(
                    settings, 'TRACKING_ANALYZER_MAXMIND_CITIES')
            except AttributeError:
                raise CommandError(
                    '`TRACKING_ANALYZER_MAXMIND_CITIES` setting not '
                    'present. Unable to get the GeoIP dataset.'
                )

        self.checkout_datasets(geoip_dir, url, [countries, cities])
