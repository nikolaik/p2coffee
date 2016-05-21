from datetime import timedelta

from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import task, periodic_task, db_task
from p2coffee.models import SensorEvent


@db_task()
def on_new_meter(logevent):
    print(logevent)
    timeinterval = timedelta(minutes=5)
    if SensorEvent.objects.filter(created__gt=timezone.now() - timeinterval):
        pass


@periodic_task(crontab(minute='*/5'))
# OR db_periodic_task
def test_noop_task():
    print("doing nothing")
    pass