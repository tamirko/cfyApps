# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-09 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rms', '0005_auto_20170809_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='allocatedresources',
            name='group_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
