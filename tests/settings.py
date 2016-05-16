import os

SECRET_KEY = 'django_tracking_analyzer_secret'

DATABASES = {
    'default': {
        # Memory resident database, for easy testing.
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'tracking_analyzer',
    'tests'
]

# Django GIS GeoIP2 settings.
GEOIP_PATH = os.path.join(DJANGO_PROJECT_DIR, 'geoip_db')
