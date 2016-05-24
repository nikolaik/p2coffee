from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from p2coffee.models import SensorEvent, CoffeePotEvent


class CoffeePotEventAdmin(admin.ModelAdmin):
    list_display = ['type', 'created_precise']
    list_filter = ['type']
    readonly_fields = ['uuid', 'created']

    def created_precise(self, obj):
        return obj.created.strftime("%Y-%m-%d %H:%M:%S")

    created_precise.admin_order_field = 'created'
    created_precise.short_description = _('Created')


class SensorEventAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name', 'id', 'value', 'created_precise']
    list_filter = ['name', 'id']
    readonly_fields = ['uuid', 'created']
    fields = ['name', 'id', 'value', 'uuid', 'created']

    def created_precise(self, obj):
        return obj.created.strftime("%Y-%m-%d %H:%M:%S")

    created_precise.admin_order_field = 'created'
    created_precise.short_description = _('Created')


admin.site.register(CoffeePotEvent, CoffeePotEventAdmin)
admin.site.register(SensorEvent, SensorEventAdmin)
