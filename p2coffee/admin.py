from django.contrib import admin

from p2coffee.models import SensorEvent, CoffeePotEvent


class CoffeePotEventAdmin(admin.ModelAdmin):
    list_display = ['type', 'created']
    list_filter = ['type']
    readonly_fields = ['uuid', 'created']


class SensorEventAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name', 'id', 'value', 'created']
    list_filter = ['name', 'id']
    readonly_fields = ['uuid', 'created']
    fields = ['name', 'id', 'value', 'uuid', 'created']


admin.site.register(CoffeePotEvent, CoffeePotEventAdmin)
admin.site.register(SensorEvent, SensorEventAdmin)
