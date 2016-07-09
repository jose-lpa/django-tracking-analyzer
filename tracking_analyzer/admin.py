import json

from django.conf.urls import patterns, url
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.views.generic import TemplateView

from django_countries import countries

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
        ('timestamp', admin.DateFieldListFilter), 'device_type', 'user'
    ]
    list_display = [
        'content_object', 'timestamp', 'ip_address', 'ip_country', 'ip_city',
        'user_link',
    ]
    ordering = ['-timestamp']

    def user_link(self, obj):
        if obj.user:
            return '<a href="{0}?user__id__exact={1}">{2}</a>'.format(
                reverse('admin:tracking_analyzer_tracker_changelist'),
                obj.user.pk,
                obj.user
            )
        else:
            return 'Anonymous'

    user_link.allow_tags = True
    user_link.short_description = 'User'

    def has_add_permission(self, request):
        """
        Overrides base ``has_add_permission`` method to block up any admin user
        create actions. ``Tracker`` instances are only data to be seen or
        deleted.
        """
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Overrides base ``change_view`` method to block up any admin user create
        or update actions. ``Tracker`` instances are only data to be seen or
        deleted.
        """
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

    def changelist_view(self, request, extra_context=None):
        """
        Overrides base ``changelist_view`` method to add analytics datasets to
        the response.
        """
        extra_context = extra_context or {}
        countries_count = []
        response = super().changelist_view(request, extra_context)

        # Get the current objects queryset to analyze data from it.
        queryset = response.context_data['cl'].queryset

        # Requests per country.
        trackers = queryset.values('ip_country').annotate(
            trackers=Count('id')).order_by()
        for tracker in trackers:
            countries_count.append(
                [countries.alpha3(tracker['ip_country']), tracker['trackers']])

        extra_context['countries_count'] = json.dumps(countries_count)

        # Requests by device (when not filtering by device).
        if 'device_type__exact' not in request.GET:
            devices_count = queryset.values('device_type').annotate(
                count=Count('id')).order_by()

            extra_context['devices_count'] = json.dumps(list(devices_count))

        response.context_data.update(extra_context)

        return response

    def get_urls(self):
        urls = super(TrackerAdmin, self).get_urls()
        my_urls = patterns(
            '',
            url(r'stats/$', self.admin_site.admin_view(StatisticsDashboard.as_view()), name='stats_dashboard'),
        )
        return my_urls + urls


admin.site.register(Tracker, TrackerAdmin)
