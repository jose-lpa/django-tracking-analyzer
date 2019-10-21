from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import re_path


admin.autodiscover()


urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
