from django import forms

from .models import Tweet


class CreateTweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ["text"]

    def save(self, commit=True):
        tweet = super().save(commit=False)
        tweet.author = self.instance.user  # Set the author to the current user
        if commit:
            tweet.save()
        return tweet
