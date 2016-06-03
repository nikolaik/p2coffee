from huey.contrib.djhuey import db_task

from p2coffee import slack
from p2coffee.models import SensorEvent, CoffeePotEvent


def on_new_meter(sensor_event):
    assert isinstance(sensor_event, SensorEvent)
    # FIXME values are guesstimates
    threshold_started = 1500
    threshold_finished = 100
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
    elif current_value <= threshold_finished < previous_value:
        cpe = CoffeePotEvent.objects.create(type=CoffeePotEvent.BREWING_FINISHED)

    if cpe is not None:
        send_to_slack(cpe)


@db_task()
def send_to_slack(cpe):
    # Notify on Slack
    slack.send_msg(cpe.as_slack_text())
