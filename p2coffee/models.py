from django.db import models
from django_extensions.db.models import TimeStampedModel
import uuid


class SensorEvent(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=254)
    value = models.CharField(max_length=254)
    id = models.CharField(max_length=254)

    def __str__(self):
        return str(self.uuid)
