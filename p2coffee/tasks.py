from datetime import timedelta

from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import task, periodic_task, db_task
from p2coffee.models import SensorEvent


@db_task()
def on_new_meter(sensor_event):
    print(sensor_event)
    timeinterval = timedelta(minutes=5)
    if SensorEvent.objects.filter(created__gt=timezone.now() - timeinterval):
        pass
        # TODO do something


@periodic_task(crontab(minute='*/5'))
# OR db_periodic_task
def test_noop_task():
    print("doing nothing")
    pass