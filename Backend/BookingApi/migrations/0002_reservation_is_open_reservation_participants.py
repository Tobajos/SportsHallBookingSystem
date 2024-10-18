# Generated by Django 5.1.2 on 2024-10-18 10:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingApi', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_open',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservation',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='joined_reservations', to=settings.AUTH_USER_MODEL),
        ),
    ]
