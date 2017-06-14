# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

# python manage.py makemigrations rms

# Create your models here.

#class Choice(models.Model):
#    question = models.ForeignKey(Question, on_delete=models.CASCADE)
#    choice_text = models.CharField(max_length=200)
#    votes = models.IntegerField(default=0)


@python_2_unicode_compatible  # only if you need to support Python 2
class ResourceTypes(models.Model):
    resource_id = models.AutoField(primary_key=True)
    resource_name = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=200)
    resource_version = models.CharField(max_length=200)
    total_quantity = models.IntegerField()
    available_quantity = models.IntegerField(default=total_quantity)
    resource_description = models.CharField(max_length=400)
    is_external = models.NullBooleanField(default=False)
    resource_extra_fields = models.CharField(max_length=400)

    def __str__(self):
        return "{0}-{1}-{2}".format(self.resource_name, self.resource_type, self.resource_version)


@python_2_unicode_compatible  # only if you need to support Python 2
class AllocatedResources(models.Model):
    allocation_id = models.AutoField(primary_key=True)
    resource_id = models.ForeignKey(ResourceTypes, on_delete=models.CASCADE)
    parent_allocation_id = models.IntegerField()
    allocation_time = models.DateTimeField('Allocation date')
    expiration_time = models.DateTimeField('Expiration  date')
    allocation_description = models.CharField(max_length=400)
    tenant_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
    allocation_extra_fields = models.CharField(max_length=400)

    def __str__(self):
        return "{0}-{1}-{2}".format(self.resource_name, self.tenant_name, self.user_name)