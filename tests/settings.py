import os


TESTING_DIR = os.path.abspath(os.path.dirname(__file__))

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
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'tracking_analyzer',
    'tests'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    },
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # External middleware.
    'django_user_agents.middleware.UserAgentMiddleware',
]

# Django GIS GeoIP2 settings.
# This setting is Django-mandatory to make use of GeoIP2 facilities. We are
# mocking the `GeoIP2.city()` method in the unit tests, so it's not necessary
# to download and set up the MaxMind databases.
GEOIP_PATH = TESTING_DIR

# Django Tracking Analyzer settings.
TRACKING_ANALYZER_MAXMIND_URL = "http://geolite.maxmind.com/download/geoip/database/"
TRACKING_ANALYZER_MAXMIND_COUNTRIES = "GeoLite2-Country.mmdb.gz"
TRACKING_ANALYZER_MAXMIND_CITIES = "GeoLite2-City.mmdb.gz"
