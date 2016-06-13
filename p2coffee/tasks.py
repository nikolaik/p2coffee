import logging
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from huey.contrib.djhuey import db_task, task
from p2coffee import slack
from p2coffee.models import SensorEvent, CoffeePotEvent
from p2coffee.utils import format_local_timestamp

logger = logging.getLogger(__name__)


def on_new_meter(sensor_event):
    assert isinstance(sensor_event, SensorEvent)
    # FIXME values are guesstimates
    threshold_started = 1500
    threshold_finished = 500
    cpe = None
    current_value = float(sensor_event.value)

    if sensor_event.name != SensorEvent.NAME_METER_HAS_CHANGED:
        return  # Only changes are significant, ignore normal readings

    # Get previous event value
    change_events = SensorEvent.objects.filter(
            name=SensorEvent.NAME_METER_HAS_CHANGED,
            created__lt=sensor_event.created,
    ).order_by('created')
    previous_value = float(change_events.exclude(uuid=sensor_event.uuid).last().value)

    # Compare current with previous and check if thresholds have been crossed
    if current_value >= threshold_started > previous_value:
        cpe = CoffeePotEvent.objects.create(type=CoffeePotEvent.BREWING_STARTED)
        start_brewing(cpe)
    elif current_value <= threshold_finished < previous_value:
        cpe = CoffeePotEvent.objects.create(type=CoffeePotEvent.BREWING_FINISHED)


@task()
def start_brewing(event):
    logger.debug('Starting brewing')
    channel = settings.SLACK_CHANNEL
    response = slack.chat_post_message(channel, __create_message_prefix(event))

    event.slack_channel = response['channel']
    event.slack_ts = response['ts']
    event.save()

    update_progress.schedule(args=(event.pk,), delay=3)


@db_task()
def update_progress(event_pk):
    logger.debug('Updating progress')
    try:
        event = CoffeePotEvent.objects.get(pk=event_pk)
    except CoffeePotEvent.DoesNotExist:
        logger.error("Critical error! CoffeePotEvent %d doesn't exist.", event_pk)
        return

    message = __create_message_prefix(event)
    newer_events = CoffeePotEvent.objects.filter(created__gt=event.created).order_by('created')
    if len(newer_events) == 0:
        duration = (timezone.now() - event.created).seconds
        avg_brewtime = settings.BREWTIME_AVG_MINUTES * 60

        if duration > avg_brewtime:
            message = "{0}{1}\n{2}".format(
                message,
                _("...looks like I'm a bit slow today..."),
                __create_progress_bar(100),
            )
        else:
            progress = int(100 * (duration / avg_brewtime))
            message = "{0}\n{1}".format(
                message,
                __create_progress_bar(progress),
            )

        slack.chat_update(event.slack_channel, event.slack_ts, message)
        update_progress.schedule(args=(event_pk,), delay=3)
        return

    for new_event in newer_events:
        if new_event.type == CoffeePotEvent.BREWING_FINISHED:
            t = format_local_timestamp(new_event.created, '%H:%M:%S')
            message = "{0}{1}".format(
                message,
                _(" and finished at {}!".format(t)),
            )
            slack.chat_update(event.slack_channel, event.slack_ts, message)
            return

    # Multiple brewings started without finishing. This shouldn't happen.
    raise RuntimeError('Invalid coffee pot state.')


def __create_message_prefix(event):
    t = format_local_timestamp(event.created, '%H:%M:%S')
    return _('I started brewing at {}').format(t)


def __create_progress_bar(percent):
    assert 0 <= percent <= 100
    symbol_filled = '☕'
    symbol_unfilled = '_'
    max_width = 32

    normalized = int((percent / 100) * max_width)

    filled_chars = ''.join([symbol_filled] * normalized)
    unfilled_chars = ''.join([symbol_unfilled] * (max_width - normalized))

    return '`[{}{}] {}%`'.format(filled_chars, unfilled_chars, percent)

