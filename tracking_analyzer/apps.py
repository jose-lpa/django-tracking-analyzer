from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TrackingAnalyzerAppConfig(AppConfig):
    name = 'tracking_analyzer'
    verbose_name = _('Django Tracking Analyzer')

    def ready(self):
        from . import conf  # noqa
