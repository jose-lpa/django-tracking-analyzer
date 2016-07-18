from __future__ import unicode_literals

from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/', TemplateView.as_view(template_name='base.html')),
)

urlpatterns += staticfiles_urlpatterns()
