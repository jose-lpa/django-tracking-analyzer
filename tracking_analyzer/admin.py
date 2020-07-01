import json

from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from django_countries import countries

from .utils import get_requests_count
from .models import Tracker


class TrackerAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    raw_id_fields = ['user']
    readonly_fields = [
        'content_type', 'object_id', 'ip_address', 'ip_country', 'ip_region',
        'ip_city', 'referrer', 'device_type', 'device', 'browser',
        'browser_version', 'system', 'system_version', 'user'
    ]
    list_filter = [
        ('timestamp', admin.DateFieldListFilter), 'device_type', 'content_type'
    ]
    list_display = [
        'details', 'content_object_link', 'timestamp', 'ip_address_link',
        'ip_country_link', 'ip_city_link', 'user_link',
    ]
    ordering = ['-timestamp']

    class Media:
        js = [
            'admin/js/vendor/d3/d3.min.js',
            'admin/js/vendor/topojson/topojson.min.js',
            'admin/js/vendor/datamaps/datamaps.world.min.js',
            'admin/js/vendor/d3-tip/d3-tip.min.js'
        ]

    def details(self, obj):
        """
        Define the 'Details' column rows display.
        """
        return format_html('<a href="{0}">Details</a>'.format(
            reverse('admin:tracking_analyzer_tracker_change', args=(obj.pk,))))

    details.allow_tags = True
    details.short_description = 'Details'

    def content_object_link(self, obj):
        """
        Define the 'Content Object' column rows display.
        """
        return format_html(
            '<a href="{0}?content_type__id__exact={1}&object_id__exact={2}">'
            '{3}</a>'.format(
                reverse('admin:tracking_analyzer_tracker_changelist'),
                obj.content_type.id,
                obj.object_id,
                obj
            )
        )

    content_object_link.allow_tags = True
    content_object_link.short_description = 'Content object'

    def ip_address_link(self, obj):
        """
        Define the 'IP Address' column rows display.
        """
        if obj.ip_address:
            return format_html(
                '<a href="{0}?ip_address__exact={1}">{1}</a>'.format(
                    reverse('admin:tracking_analyzer_tracker_changelist'),
                    obj.ip_address,
                )
            )

        return '-'

    ip_address_link.allow_tags = True
    ip_address_link.short_description = 'IP Address'

    def ip_country_link(self, obj):
        """
        Define the 'IP Country' column rows display.
        """
        if obj.ip_country:
            return format_html(
                '<a href="{0}?ip_country__exact={1}">{2}</a>'.format(
                    reverse('admin:tracking_analyzer_tracker_changelist'),
                    obj.ip_country,
                    obj.ip_country.name
                )
            )

        return '-'

    ip_country_link.allow_tags = True
    ip_country_link.short_description = 'IP Country'

    def ip_city_link(self, obj):
        """
        Define the 'IP City' column rows display.
        """
        if obj.ip_city:
            return format_html(
                '<a href="{0}?ip_city__exact={1}">{1}</a>'.format(
                    reverse('admin:tracking_analyzer_tracker_changelist'),
                    obj.ip_city,
                )
            )

        return '-'

    ip_city_link.allow_tags = True
    ip_city_link.short_description = 'IP City'

    def user_link(self, obj):
        """
        Define the 'User' column rows display.
        """
        if obj.user:
            return format_html(
                '<a href="{0}?user__id__exact={1}">{2}</a>'.format(
                    reverse('admin:tracking_analyzer_tracker_changelist'),
                    obj.user.pk,
                    obj.user
                )
            )

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

        return super(TrackerAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        """
        Overrides base ``changelist_view`` method to add analytics datasets to
        the response.
        """
        extra_context = extra_context or {}
        countries_count = []
        response = super(TrackerAdmin, self).changelist_view(
            request, extra_context)

        if request.method == 'GET':
            # Get the current objects queryset to analyze data from it.
            queryset = response.context_data['cl'].queryset

            # Requests by country (when no filtering by country).
            if 'ip_country__exact' not in request.GET:
                trackers = queryset.values('ip_country').annotate(
                    trackers=Count('id')).order_by()
                for track in trackers:
                    countries_count.append(
                        [countries.alpha3(track['ip_country']),
                         track['trackers']]
                    )

                extra_context['countries_count'] = json.dumps(countries_count)

            # Requests by device (when not filtering by device).
            if 'device_type__exact' not in request.GET:
                devices_count = list(queryset.values('device_type').annotate(
                    count=Count('id')).order_by())

                extra_context['devices_count'] = json.dumps(devices_count)

            # Requests time line for the current page changelist.
            current_page = response.context_data['cl'].page_num
            current_pks = response.context_data['cl'].paginator.page(
                current_page + 1).object_list.values_list('pk', flat=True)

            current_results = get_requests_count(
                Tracker.objects.filter(pk__in=list(current_pks)))

            for item in current_results:
                item['date'] = '{date}T{hour:02d}:{minute:02d}'.format(
                    date=item.pop('date'),
                    hour=item.pop('hour'),
                    minute=item.pop('minute')
                )

            extra_context['requests_count'] = json.dumps(list(current_results))

            response.context_data.update(extra_context)

        return response


admin.site.register(Tracker, TrackerAdmin)
