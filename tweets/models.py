from django.conf import settings
from django.db import models


class Tweet(models.Model):
    text = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
