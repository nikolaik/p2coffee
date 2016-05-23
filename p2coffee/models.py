from datetime import timedelta

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
import uuid


class SensorEvent(TimeStampedModel):
    NAME_SWITCH = 'power-switch'
    NAME_METER_HAS_CHANGED = 'power-meter-has-changed'
    NAME_METER = 'power-meter'

    NAME_CHOICES = [
        (NAME_SWITCH, _('Power switched')),
        (NAME_METER, _('Power metered')),
        (NAME_METER_HAS_CHANGED, _('Power meter changed'))
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=254, choices=NAME_CHOICES)
    value = models.CharField(max_length=254)
    id = models.CharField(max_length=254)

    def __str__(self):
        return str(self.uuid)


class CoffeePotEvent(TimeStampedModel):
    BREWING_STARTED = 'brew_started'
    BREWING_FINISHED = 'brew_finished'
    EVENT_TYPES = [
        (BREWING_STARTED, _('brewing started')),
        (BREWING_FINISHED, _('brewing finished'))
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=254, choices=EVENT_TYPES)

    def as_slack_text(self):
        return '{} {}{}'.format(self.__str__(), naturaltime(self.created), self._get_eta())

    def _get_eta(self):
        eta = ''

        if self.type == self.BREWING_STARTED:
            brew_time = timedelta(minutes=settings.BREWTIME_AVG_MINUTES)
            eta = _(' and should be done {}'.format(naturaltime(self.created + brew_time)))

        return eta

    def __str__(self):
        return str(dict(self.EVENT_TYPES).get(self.type))
