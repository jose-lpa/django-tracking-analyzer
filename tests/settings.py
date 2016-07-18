SECRET_KEY = 'django_tracking_analyzer_secret'

DATABASES = {
    'default': {
        # Memory resident database, for easy testing.
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'tests.urls'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
    'tracking_analyzer',
    'tests'
]

# Django GIS GeoIP2 settings.
# This setting is Django-mandatory to make use of GeoIP2 facilities. We are
# mocking the `GeoIP2.city()` method in the unit tests, so it's not necessary
# to download and set up the MaxMind databases.
GEOIP_PATH = 'tests'
