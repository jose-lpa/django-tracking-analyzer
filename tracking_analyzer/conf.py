from __future__ import unicode_literals

from django.conf import settings  # noqa

from appconf import AppConf


class TrackingAnalyzerAppConf(AppConf):
    """
    Configuration settings for Django Tracking Analyzer.

    - ``MAXMIND_URL``: The MaxMind datasets URL.
    - ``MAXMIND_DATABASE``: The file name of the MaxMind Country dataset.
    """
    MAXMIND_URL = "http://geolite.maxmind.com/download/geoip/database/"
    MAXMIND_DATABASE = "GeoLite2-Country.mmdb.gz"
