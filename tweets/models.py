from django.conf import settings
from django.db import models


class Tweet(models.Model):
    text = models.TextField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Tweet id {self.id}"
