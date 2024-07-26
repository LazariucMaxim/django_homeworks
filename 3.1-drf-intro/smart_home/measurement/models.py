from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    created_at = models.TimeField(auto_now_add=True)
