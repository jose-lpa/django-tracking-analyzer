from __future__ import unicode_literals

from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
