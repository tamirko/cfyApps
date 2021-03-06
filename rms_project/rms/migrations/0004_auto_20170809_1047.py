# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-09 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rms', '0003_auto_20170614_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocatedresources',
            name='current_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='resourcetypes',
            name='cost_per_unit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
