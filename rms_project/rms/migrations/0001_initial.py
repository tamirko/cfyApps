# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-14 11:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllocatedResources',
            fields=[
                ('allocation_id', models.AutoField(primary_key=True, serialize=False)),
                ('parent_allocation_id', models.IntegerField()),
                ('allocation_time', models.DateTimeField(verbose_name='date published')),
                ('resource_description', models.CharField(max_length=400)),
                ('expiration_time', models.DateTimeField(verbose_name='date published')),
                ('tenant_name', models.CharField(max_length=50)),
                ('user_name', models.CharField(max_length=50)),
                ('allocation_extra_fields', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceTypes',
            fields=[
                ('resource_id', models.AutoField(primary_key=True, serialize=False)),
                ('resource_name', models.CharField(max_length=200)),
                ('resource_type', models.CharField(max_length=200)),
                ('resource_version', models.CharField(max_length=200)),
                ('total_quantity', models.IntegerField()),
                ('available_quantity', models.IntegerField(default=models.IntegerField())),
                ('resource_description', models.CharField(max_length=400)),
                ('is_external', models.NullBooleanField(default=False)),
                ('resource_extra_fields', models.CharField(max_length=400)),
            ],
        ),
        migrations.AddField(
            model_name='allocatedresources',
            name='resource_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rms.ResourceTypes'),
        ),
    ]
