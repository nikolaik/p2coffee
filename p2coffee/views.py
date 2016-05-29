from braces.views import CsrfExemptMixin
from collections import defaultdict
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.translation import ugettext as _
from django.views.generic import View, TemplateView
from itertools import groupby
from rest_framework.response import Response
from rest_framework.views import APIView
from p2coffee.forms import SensorEventForm, SlackOutgoingForm
from p2coffee.models import SensorEvent, CoffeePotEvent
from p2coffee.tasks import on_new_meter


class CreateSensorEventView(View):
    """
        Logs a sensor event and runs on_new_meter task

        EXAMPLE request:
            GET /event/log/?name=power-meter-has-changed&id=ZWayVDev_zway_2-0-49-4&value=4.6
    """
    def get(self, request, *args, **kwargs):
        form = SensorEventForm(request.GET)

        if not form.is_valid():
            return HttpResponseBadRequest('Curse you coffeepot!')

        event = form.save()

        on_new_meter(event)

        return HttpResponse('Thank you coffepot!')


class StatsView(TemplateView):
    template_name = 'p2coffee/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'last_state': self._get_last_power_state(),
            'last_brew': self._get_last_coffee_event(),
            'urls': {
                'stats-events': reverse('stats-events')
            }
        })

        return context

    def _get_last_power_state(self):
        return SensorEvent.objects.filter(name=SensorEvent.NAME_SWITCH).last()

    def _get_last_coffee_event(self):
        return CoffeePotEvent.objects.last()


class StatsEvents(APIView):
    """List events grouped by name, in highcharts friendly format."""
    def get(self, request, format=None):
        return Response(self._get_events_by_hour())

    def _get_events_by_hour(self):
        queryset = SensorEvent.objects.filter(name=SensorEvent.NAME_METER_HAS_CHANGED, value__gt=0)
        queryset = queryset.order_by('created')
        events = queryset.values('value', 'created')

        # First, split all events into days
        events_by_date = defaultdict(list)
        for event in events:
            key = event['created'].date().isoformat()
            events_by_date[key].append(event)

        # Format right now:
        # events_by_date = {"2016-05-01": [event, event, ...], ...}
        #
        # Desired format:
        # event_series = [
        #   {
        #     "name":
        #     "data": [ ["00:00": <value>], ["01:00"], ]
        #   }
        # ]

        event_series = []
        for date, events in events_by_date.items():
            event_series.append({
                "name": date,
                "data": self._events_to_highcharts_format(
                    events,
                )
            })
        return event_series

    def _get_events(self):
        events = SensorEvent.objects.filter(name=SensorEvent.NAME_METER_HAS_CHANGED).values('name', 'value', 'created')

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

    def _events_to_highcharts_format(self, events, x_function=None, y_function=None):
        if x_function is None:
            x_function = lambda e: e['created'].timestamp() * 1000
        if y_function is None:
            y_function = lambda e: float(e['value'])

        return list(map(lambda e: [x_function(e), y_function(e)], events))


class SlackOutgoingView(CsrfExemptMixin, View):
    def post(self, request):
        form = SlackOutgoingForm(request.POST)

        if not form.is_valid():
            return JsonResponse({'text': 'Invalid form'}, status=400)

        user_name = form.cleaned_data['user_name']

        # TODO: check form.cleaned_data['text']
        last_event = CoffeePotEvent.objects.last()
        brewing_status = _('I\'m a coffee pot!')
        if last_event:
            brewing_status = last_event.as_slack_text()

        return JsonResponse({'text': _('Hi {}, {}').format(user_name, brewing_status)})
