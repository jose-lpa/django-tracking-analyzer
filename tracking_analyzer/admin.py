from django.conf.urls import patterns, url
from django.contrib import admin
from django.views.generic import TemplateView

from .models import Tracker


class StatisticsDashboard(TemplateView):
    template_name = 'admin/stats_dashboard.html'


class TrackerAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    raw_id_fields = ['user']
    readonly_fields = [
        'content_type', 'object_id', 'ip_address', 'ip_country', 'ip_region',
        'ip_city', 'referrer', 'device_type', 'device', 'browser',
        'browser_version', 'system', 'system_version', 'user'
    ]
    list_filter = [
        ('timestamp', admin.DateFieldListFilter), 'device_type'
    ]
    list_display = [
        'content_object', 'timestamp', 'ip_address', 'ip_country', 'ip_city',
        'user',
    ]

    # Block up any admin user create actions. `Tracker` instances are
    # only data units to be seen or deleted.
    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(
            {
                'show_save_and_add_another': False,
                'show_save_and_continue': False,
                'show_save': False
            }
        )

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context)

    def get_urls(self):
        urls = super(TrackerAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'stats/$', self.admin_site.admin_view(StatisticsDashboard.as_view()), name='stats_dashboard'),
        )
        return my_urls + urls


admin.site.register(Tracker, TrackerAdmin)
