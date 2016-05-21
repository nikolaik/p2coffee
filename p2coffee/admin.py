from django.contrib import admin

from p2coffee.models import SensorEvent


class SensorEventAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name', 'id', 'value', 'created']
    list_filter = ['name', 'id']
    readonly_fields = ['uuid', 'created']
    fields = ['name', 'id', 'value', 'uuid', 'created']


admin.site.register(SensorEvent, SensorEventAdmin)
