from django import forms
from django.contrib.auth import get_user_model

Tweet = get_user_model()


class CreateTweetForm(forms.Form):
    class Meta:
        model = Tweet
        fields = ("text", "timestamp", "author")
