from django.core.management.base import BaseCommand, CommandError
from p2coffee.forms import SensorEventForm
from p2coffee.models import SensorEvent
import logging
import random
import requests
import urllib
import uuid


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    EV_POWER_SWITCH = 'power-switch'
    EV_POWER_VALUE = 'power-meter-has-changed'
    EV_POWER_METER = 'power-meter'

    EV_STATE_TRANSITIONS = {
        None: [EV_POWER_SWITCH],
        EV_POWER_SWITCH: [EV_POWER_VALUE],
        EV_POWER_VALUE: [EV_POWER_VALUE],
        EV_POWER_METER: [],
    }

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        event = SensorEvent.objects.order_by('created').last()
        if event:
            self.current_state = event.name
        else:
            self.current_state = None

    def add_arguments(self, parser):
        parser.add_argument('-H', '--host', nargs='?', default='127.0.0.1')
        parser.add_argument('-P', '--port', nargs='?', default='8000')

    def handle(self, *args, **kwargs):
        host = kwargs['host']
        port = kwargs['port']
        self._simulate_single(host, port)  # TODO: Make it a loop


    def _simulate_single(self, host, port):
        data = self._create_event()
        response = self._send_event(host, port, data)
        logger.info("Request sent! Returned status code: %d", response.status_code)
        if response.status_code >= 400:
            logger.warning("Request failed (%d)! Content of the response:\n%s", response.status_code, str(response.content))


    def _create_event(self):
        new_state = random.choice(self.EV_STATE_TRANSITIONS[self.current_state])
        if new_state == self.EV_POWER_SWITCH:
            value = 'on'
        elif new_state == self.EV_POWER_VALUE:
            value = str(int(min(255, max(0, random.gauss(128, 64)))))
        return {
            'name': new_state,
            'value': value,
            'id': str(uuid.uuid4()),
        }

    def _send_event(self, host, port, data):
        url = urllib.parse.urljoin("http://{}:{}".format(host, port), '/event/log/')
        return requests.get(url, params=data)

