# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question, Choice

# Register your models here.

admin.site.register(Question)
admin.site.register(Choice)
admin.site.site_header = "Resource Management System header"
admin.site.site_header = "Resource Management System"
#admin.site.index_title = "This is my index_title"