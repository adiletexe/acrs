from django.db import models
from django.utils.timezone import now

# Create your models here.
class Containers(models.Model):
    color = models.CharField(max_length=10, default="nothing")
    time = models.DateTimeField(default=now)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

class Position(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    steps_left = models.IntegerField(blank=True)
    currentname = models.CharField(max_length=100, blank=True)
