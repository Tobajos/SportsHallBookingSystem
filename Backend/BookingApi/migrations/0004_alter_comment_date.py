# Generated by Django 5.1.2 on 2024-11-15 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingApi', '0003_alter_post_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
