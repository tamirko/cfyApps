# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-14 12:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allocatedresources',
            name='allocation_time',
            field=models.DateTimeField(verbose_name='Allocation date'),
        ),
        migrations.AlterField(
            model_name='allocatedresources',
            name='expiration_time',
            field=models.DateTimeField(verbose_name='Expiration  date'),
        ),
    ]
