from __future__ import unicode_literals

from django.urls import include, path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()


urlpatterns = [
    path(r'admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
