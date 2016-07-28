from __future__ import (
    division, absolute_import, print_function, unicode_literals
)

import os
import gzip

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from tracking_analyzer.compat import HTTPError, URLError, urlopen


class Command(BaseCommand):
    help = 'Installs/updates the MaxMind(R) Country dataset. Plase check ' \
           'https://www.maxmind.com/ for more information.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            help='Base URL where the MaxMind(R) Country dataset is available.'
                 ' Optional, probably better not to use it.'
        )
        parser.add_argument(
            '--dataset',
            help='Remote file name for the MaxMind(R) Country dataset.'
                 ' Optional, probably better not to use it.'
        )

    def user_input(self):
        """
        Helper method to handle user input when required.
        """
        if input('(y/n) ').lower() in ['y', 'yes']:
            return True
        else:
            return False

    def install_dataset(self, geoip_dir, mm_url, mm_dataset):
        """
        Downloads the MaxMind Country dataset and unpacks it into the selected
        Django project ``GEOIP_PATH`` directory.

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

        filename = os.path.join(geoip_dir, mm_dataset)

        with open(filename, 'wb') as f:
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
                f.write(buffer)

                status = "{0:16}".format(file_size_dl)
                if file_size:
                    status += " downloaded [{0:6.2f}%]".format(
                        file_size_dl * 100 / file_size)
                status += chr(13)
                print(status, end="")
            print()

        self.stdout.write('Uncompressing downloaded dataset...')

        with gzip.open(filename, 'rb') as gzipped:
            with open(os.path.splitext(filename)[0], 'wb') as gunzipped:
                gunzipped.write(gzipped.read())
                self.stdout.write(
                    '{0} dataset installed and ready for use.'.format(
                        os.path.splitext(filename)[0]
                    )
                )

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

        ds = options.get('dataset')
        if not ds:
            # Check `TRACKING_ANALYZER_MAXMIND_DATABASE` setting is ready.
            try:
                ds = getattr(settings, 'TRACKING_ANALYZER_MAXMIND_DATABASE')
            except AttributeError:
                raise CommandError(
                    '`TRACKING_ANALYZER_MAXMIND_DATABASE` setting not present.'
                    ' Unable to get the GeoIP dataset.'
                )

        if os.path.isfile(os.path.join(geoip_dir, os.path.splitext(ds)[0])):
            self.stdout.write(
                'Seems that MaxMind dataset is already installed in "{0}". Do '
                'you want to reinstall it?'.format(geoip_dir)
            )

            if self.user_input() is True:
                self.stdout.write('Updating MaxMind Country dataset...')
                self.install_dataset(geoip_dir, mm_url=url, mm_dataset=ds)
            else:
                self.stdout.write('Country dataset should be ready.')
        else:
            self.stdout.write('Installing MaxMind Country dataset...')
            self.install_dataset(geoip_dir, mm_url=url, mm_dataset=ds)
