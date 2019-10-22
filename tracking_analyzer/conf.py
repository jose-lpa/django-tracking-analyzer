from django.conf import settings  # pylint: disable=unused-import

from appconf import AppConf


class TrackingAnalyzerAppConf(AppConf):
    """
    Configuration settings for Django Tracking Analyzer.

    - ``MAXMIND_URL``: The MaxMind datasets URL.
    - ``MAXMIND_COUNTRIES``: The file name of the MaxMind Country dataset.
    - ``MAXMIND_CITIES``: The file name of the MaxMind City dataset.
    """
    MAXMIND_URL = "http://geolite.maxmind.com/download/geoip/database/"
    MAXMIND_COUNTRIES = "GeoLite2-Country.mmdb.gz"
    MAXMIND_CITIES = "GeoLite2-City.mmdb.gz"
