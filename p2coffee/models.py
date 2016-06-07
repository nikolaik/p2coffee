from datetime import timedelta

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.utils.timesince import timesince
from django.utils.translation import ugettext_lazy as _, ugettext
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

    class Meta:
        verbose_name = _('Sensor event')
        verbose_name_plural = _('Sensor events')
        index_together = ['created', 'modified']
        ordering = ['created']


class CoffeePotEvent(TimeStampedModel):
    BREWING_STARTED = 'brew_started'
    BREWING_FINISHED = 'brew_finished'
    EVENT_TYPES = [
        (BREWING_STARTED, _('I started brewing')),
        (BREWING_FINISHED, _('I\'m done brewing'))
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=254, choices=EVENT_TYPES)
    slack_channel = models.CharField(max_length=64, null=True, blank=True)
    slack_ts = models.CharField(max_length=64, null=True, blank=True)

    @staticmethod
    def _naturaltime_with_for(dt):
        """ prefixes with 'for' when dt in the past and language is norwegian """
        dt_natural = naturaltime(dt)

        if settings.LANGUAGE_CODE != 'nb':
            return dt_natural

        # If not now and not in the future
        if dt_natural != ugettext('now') and ugettext('from') not in dt_natural:
            dt_natural = '{} {}'.format(ugettext('for'), dt_natural)

        return dt_natural

    def as_text(self):
        return self.as_slack_text()

    def as_slack_text(self):
        return '{} {}{}'.format(self.__str__(), self._naturaltime_with_for(self.created), self._get_duration())

    def _get_duration(self):
        duration = ''

        if self.type == self.BREWING_STARTED:
            brew_time = timedelta(minutes=settings.BREWTIME_AVG_MINUTES)
            expected_brewtime = self._naturaltime_with_for(self.created + brew_time)
            duration = ugettext(' and should be done {}').format(expected_brewtime)

        elif self.type == self.BREWING_FINISHED:
            events_started = CoffeePotEvent.objects.filter(type=self.BREWING_STARTED)
            last_started_event = events_started.exclude(uuid=self.uuid).last()

            if last_started_event:
                actual_brew_time = timesince(last_started_event.created, self.created)
                duration = ugettext(', took only {}').format(actual_brew_time)

        return duration

    def __str__(self):
        return str(dict(self.EVENT_TYPES).get(self.type))

    class Meta:
        verbose_name = _('Coffee pot event')
        verbose_name_plural = _('Coffee pot events')
        index_together = ['created', 'modified']
        ordering = ['created']
