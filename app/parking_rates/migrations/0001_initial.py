# Generated by Django 3.2 on 2021-04-20 22:58

import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time_range', django.contrib.postgres.fields.ranges.DateTimeRangeField(
                    unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]