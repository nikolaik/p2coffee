from itertools import groupby
from pprint import pprint

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View, TemplateView

from p2coffee.forms import LogEventForm
from p2coffee.models import LogEvent
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateLogEventView(View):
    # /event/log/?name=power-meter-has-changed&id=ZWayVDev_zway_2-0-49-4&value=4.6
    def get(self, request, *args, **kwargs):
        form = LogEventForm(request.GET)
        if form.is_valid():
            form.save()

        return HttpResponse('Thank you coffepot!')


class StatsView(TemplateView):
    template_name = 'p2coffee/stats.html'

    # FIXME settings
    NAME_SWITCH = 'power-switch'
    NAME_METER_HAS_CHANGED = 'power-meter-has-changed'
    NAME_METER = 'power-meter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'last_state': self._get_last_power_state(),
            'urls': {
                'stats-events': reverse('stats-events')
            }
        })

        return context

    def _get_last_power_state(self):
        return LogEvent.objects.filter(name=self.NAME_SWITCH).order_by('created').last()


class StatsEvents(APIView):
    """List events grouped by name, in highcharts friendly format."""
    def get(self, request, format=None):
        return Response(self._get_events())

    def _get_events(self):
        events = LogEvent.objects.exclude(name=StatsView.NAME_SWITCH).values('name', 'value', 'created')

        # Group the data
        keyfunc = lambda x: x['name']
        event_groups = []
        data = sorted(events, key=keyfunc)
        for key, group in groupby(data, keyfunc):
            event_groups.append({
                'name': key,
                'data': self._events_to_highcharts_format(group)
            })

        return event_groups

    def _events_to_highcharts_format(self, events):
        return list(map(lambda e: [e['created'].timestamp() * 1000, float(e['value'])], events))
