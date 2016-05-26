from django.contrib import admin
from django.templatetags.tz import localtime
from django.utils.formats import date_format
from django.utils.translation import ugettext_lazy as _

from p2coffee.models import SensorEvent, CoffeePotEvent


def format_datetime(dt, dt_format='Y-m-d H:i:s'):
    return date_format(localtime(dt), dt_format)


class CoffeePotEventAdmin(admin.ModelAdmin):
    list_display = ['type', 'created_precise']
    list_filter = ['type']
    readonly_fields = ['uuid', 'created']
    ordering = ['-created']

    def created_precise(self, obj):
        return format_datetime(obj.created)

    created_precise.admin_order_field = 'created'
    created_precise.short_description = _('Created')


class SensorEventAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name', 'id', 'value', 'created_precise']
    list_filter = ['name', 'id']
    readonly_fields = ['uuid', 'created']
    fields = ['name', 'id', 'value', 'uuid', 'created']
    ordering = ['-created']

    def created_precise(self, obj):
        return format_datetime(obj.created)

    created_precise.admin_order_field = 'created'
    created_precise.short_description = _('Created')


admin.site.register(CoffeePotEvent, CoffeePotEventAdmin)
admin.site.register(SensorEvent, SensorEventAdmin)
