# Generated by Django 4.1.13 on 2023-11-02 11:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tweets", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tweet",
            name="text",
            field=models.TextField(max_length=280),
        ),
        migrations.AlterField(
            model_name="tweet",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
