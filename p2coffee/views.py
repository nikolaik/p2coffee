from itertools import groupby
from pprint import pprint

from django.http import HttpResponse
from django.views.generic import View, TemplateView

from p2coffee.forms import LogEventForm
from p2coffee.models import LogEvent


class CreateLogEventView(View):
    # /event/log/?name=power-meter-has-changed&id=ZWayVDev_zway_2-0-49-4&value=4.6
    def get(self, request, *args, **kwargs):
        form = LogEventForm(request.GET)
        if form.is_valid():
            form.save()

        return HttpResponse('Thank you coffepot!')


class StatsView(TemplateView):
    template_name = 'p2coffee/stats.html'

    NAME_SWITCH = 'power-switch'  # FIXME: setting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'events': self._get_events(),
            'last_state': self._get_last_power_state()
        })

        return context

    def _get_last_power_state(self):
        return LogEvent.objects.filter(name=self.NAME_SWITCH).order_by('created').last()

    def _get_events(self):
        events = LogEvent.objects.exclude(name=self.NAME_SWITCH).values('name', 'value', 'created')
        events_formatted = []
        # for name, value, created in events:
        #     events_formatted.append({
        #
        #     })

        keyfunc = lambda x: x['name']
        groups = []
        uniquekeys = []
        data = sorted(events, key=keyfunc)
        for k, g in groupby(data, keyfunc):
            groups.append(list(g))  # Store group iterator as a list
            uniquekeys.append(k)
        pprint(groups)
        pprint(uniquekeys)

        return groups