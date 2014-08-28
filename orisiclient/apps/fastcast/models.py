from django.db import models

import base64

#Create your models here.

class FastcastKey(models.Model):
  ts = models.DateTimeField(auto_now_add=True)
  pub = models.CharField(max_length=1024)
  priv = models.CharField(max_length=1024)

