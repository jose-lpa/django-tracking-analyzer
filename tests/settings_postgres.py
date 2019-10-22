# pylint: disable=wildcard-import,unused-wildcard-import
from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tracking_analyzer_test',
        'USERNAME': 'postgres',
        'PASSWORD': '',
    }
}
