# Generated by Django 4.1.13 on 2023-11-21 00:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tweets", "0002_alter_tweet_text_alter_tweet_timestamp"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tweet",
            old_name="timestamp",
            new_name="created_at",
        ),
    ]