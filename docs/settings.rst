.. _settings:

========
Settings
========

Django Tracking Analyzer behaviour can be customized by using the next
application settings in your project:

``GEOIP_PATH``
--------------

It defines the path where the GeoIP2 datasets are installed.

Although this is not a Django Tracking Analyzer setting, you have to set it up
in order to get the GeoIP datasets working properly. Please check `GeoIP2 Django documentation`_
for detailed information.

- Default: **unset**

``TRACKING_ANALYZER_MAXMIND_URL``
---------------------------------

Specifies the URL where the GeoIP datasets have to be retrieved from. It
defaults to the MaxMind database official repository.

- Default: ``'http://geolite.maxmind.com/download/geoip/database/'``

``TRACKING_ANALYZER_MAXMIND_COUNTRIES``
---------------------------------------

Specifies the file name for the *compressed* countries database.

- Default: ``'GeoLite2-Country.mmdb.gz'``

``TRACKING_ANALYZER_MAXMIND_CITIES``
------------------------------------

Specifies the file name for the *compressed* cities database.

- Default: ``'GeoLite2-City.mmdb.gz'``


.. _GeoIP2 Django documentation: https://docs.djangoproject.com/en/1.10/ref/contrib/gis/geoip2/
