from huey.contrib.djhuey import db_task

from p2coffee import slack
from p2coffee.models import SensorEvent, CoffeePotEvent


@db_task()
def on_new_meter(sensor_event):
    assert isinstance(sensor_event, SensorEvent)
    # FIXME values are guesstimates
    start_treshold = 1500
    finish_treshhold = 100
    cpe = None

    # Get previous event
    change_events = SensorEvent.objects.filter(name=SensorEvent.NAME_METER_HAS_CHANGED)
    previous_event = change_events.exclude(uuid=sensor_event.uuid).order_by('created').last()

    # Compare current with previous and check if thresholds have been crossed
    if float(sensor_event.value) >= start_treshold > float(previous_event.value):
        cpe = CoffeePotEvent.objects.create(type=CoffeePotEvent.BREWING_STARTED)
    elif float(sensor_event.value) <= finish_treshhold < float(previous_event.value):
        cpe = CoffeePotEvent.objects.create(type=CoffeePotEvent.BREWING_FINISHED)

    # Notify on Slack
    if cpe is not None:
        slack.send_msg(cpe.as_slack_text())
