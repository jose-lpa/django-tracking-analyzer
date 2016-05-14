from django.contrib import admin

from .models import Tracker


class TrackerAdmin(admin.ModelAdmin):
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

    # Block up any admin user create/delete actions. Only programmers are
    # intended to create new templates via data migrations.
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
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


admin.site.register(Tracker, TrackerAdmin)
