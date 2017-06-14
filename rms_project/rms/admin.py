# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import ResourceTypes, AllocatedResources

# Register your models here.

admin.site.register(ResourceTypes)
admin.site.register(AllocatedResources)
#admin.site.site_header = "Resource Management System header 2"
#admin.site.site_header = "Resource Management System"
#admin.site.index_title = "This is my index_title"