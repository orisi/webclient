from django.db import models

# Create your models here.

class TimelockAddress(models.Model):
  ts = models.DateTimeField(auto_now_add=True)
  address = models.CharField(max_length=255)
  message_id = models.CharField(max_length=255)
  pub = models.CharField(max_length=1024)
  locktime = models.IntegerField()
