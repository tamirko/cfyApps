# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from django.template import loader
from django.http import Http404
from .models import AllocatedResources, ResourceTypes


# Create your views here.


class IndexView(generic.ListView):
    template_name = 'rms/index.html'
    context_object_name = 'latest_allocated_list'

    def get_queryset(self):
        """Return the last five allocated resources."""
        #alocation_count = AllocatedResources.objects.count()
        #return AllocatedResources.objects.order_by('-allocation_id')[:5]
        #return AllocatedResources.objects.order_by('-allocation_id')[::-1]
        #return AllocatedResources.objects.order_by('allocation_id')
        return AllocatedResources.objects.order_by('allocation_time')[::-1]


class StatsView(generic.ListView):
    template_name = 'rms/stats.html'
    context_object_name = 'latest_allocated_list'

    def get_queryset(self):
        """Return the last five allocated resources."""
        #alocation_count = AllocatedResources.objects.count()
        #return AllocatedResources.objects.order_by('-allocation_id')[:5]
        #return AllocatedResources.objects.order_by('-allocation_id')[::-1]
        #return AllocatedResources.objects.order_by('allocation_id')
        return AllocatedResources.objects.order_by('allocation_time')[::-1]


class DetailView(generic.DetailView):
    model = AllocatedResources
    template_name = 'rms/detail.html'


class ResultsView(generic.DetailView):
    model = AllocatedResources
    template_name = 'rms/results.html'


#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    context = {'latest_question_list': latest_question_list}
#    return render(request, 'polls/index.html', context)


#def index(request):
#    return HttpResponse("Hello, world. You're at the RMS index.")