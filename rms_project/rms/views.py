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


class AllocationsView(generic.ListView):
    template_name = 'rms/allocations.html'
    context_object_name = 'latest_allocated_list'

    def get_queryset(self):
        """Return the last five allocated resources."""
        #alocation_count = AllocatedResources.objects.count()
        #return AllocatedResources.objects.order_by('-allocation_id')[:5]
        #return AllocatedResources.objects.order_by('-allocation_id')[::-1]
        #return AllocatedResources.objects.order_by('allocation_id')
        return AllocatedResources.objects.order_by('allocation_time')[::-1]


def _init_alloc_dict(allocation_count):
        alloc_dict = {}
        alloc_dict["counter"] = allocation_count
        alloc_dict["cost"] = 0
        alloc_dict["tenants"] = {"entities": {}, "counter": 0,
                                 "all_users": {}, "all_users_counter": 0,
                                 "all_types": {}, "all_types_counter": 0}

        alloc_dict["users"] = {}
        alloc_dict["groups"] = {}
        alloc_dict["types"] = {"entities": {}, "counter": 0}
        return alloc_dict


def _update_highlevel_values(alloc, alloc_dict, current_cost):
    alloc_dict["cost"] += current_cost


def _update_allocation_types(alloc, alloc_dict, current_cost):
    current_type_name = alloc.resource_id.resource_type
    current_types = alloc_dict["types"]
    current_types_entities = alloc_dict["types"]["entities"]
    if current_type_name not in current_types_entities:
        current_types_entities[current_type_name] = {"cost": 0, "users": {}, "tenants": {}, "counter": 0}
        current_types["counter"] += 1

    current_type_obj = current_types_entities[current_type_name]
    current_type_obj["cost"] += current_cost
    current_type_obj["counter"] += 1
    current_type_users = current_type_obj["users"]
    current_type_tenants = current_type_obj["tenants"]

    if alloc.user_name not in current_type_users:
        current_type_users[alloc.user_name] = 0
    current_type_users[alloc.user_name] += current_cost

    if alloc.tenant_name not in current_type_tenants:
        current_type_tenants[alloc.tenant_name] = 0
    current_type_tenants[alloc.tenant_name] += current_cost


def _update_allocation_tenants(alloc, alloc_dict, current_cost, current_type_name):
    tenants = alloc_dict["tenants"]
    tenants_entities = alloc_dict["tenants"]["entities"]
    if alloc.tenant_name not in tenants_entities:
        tenants_entities[alloc.tenant_name] = {"cost": 0, "users": {}, "types": {}}
        tenants["counter"] += 1

    current_tenant = tenants_entities[alloc.tenant_name]
    current_tenant["cost"] += current_cost

    current_tenant_users = current_tenant["users"]
    if alloc.user_name not in current_tenant_users:
        current_tenant_users[alloc.user_name] = 0
    current_tenant_users[alloc.user_name] += current_cost

    if alloc.user_name not in tenants["all_users"]:
        tenants["all_users"][alloc.user_name] = True
        tenants["all_users_counter"] += 1

    current_tenant_types = current_tenant["types"]
    if current_type_name not in current_tenant_types:
        current_tenant_types[current_type_name] = 0
    current_tenant_types[current_type_name] += current_cost

    if current_type_name not in tenants["all_types"]:
        tenants["all_types"][current_type_name] = True
        tenants["all_types_counter"] += 1


def _update_allocation_users(alloc, alloc_dict, current_cost, current_type_name):
    if alloc.user_name not in alloc_dict["users"]:
        alloc_dict["users"][alloc.user_name] = {"cost": 0, "types": {}}
    current_user = alloc_dict["users"][alloc.user_name]
    current_user["cost"] += current_cost

    current_user_types = current_user["types"]
    if current_type_name not in current_user_types:
        current_user_types[current_type_name] = 0
    current_user_types[current_type_name] += current_cost


def _update_allocation_groups(alloc, alloc_dict, current_cost, current_type_name):
    if alloc.group_name not in alloc_dict["groups"]:
        alloc_dict["groups"][alloc.group_name] = {"cost": 0, "users": {}, "types": {}}
    current_group = alloc_dict["groups"][alloc.group_name]
    current_group["cost"] += current_cost

    current_group_users = current_group["users"]
    if alloc.user_name not in current_group_users:
        current_group_users[alloc.user_name] = 0
    current_group_users[alloc.user_name] += current_cost

    if current_type_name not in current_group["types"]:
        current_group["types"][current_type_name] = 0
    current_group["types"][current_type_name] += current_cost


def _update_alloc_dict(alloc, alloc_dict):
    current_cost = alloc.current_cost
    current_type_name = alloc.resource_id.resource_type

    _update_highlevel_values(alloc, alloc_dict, current_cost)

    _update_allocation_types(alloc, alloc_dict, current_cost)
    _update_allocation_tenants(alloc, alloc_dict, current_cost, current_type_name)
    _update_allocation_users(alloc, alloc_dict, current_cost, current_type_name)
    _update_allocation_groups(alloc, alloc_dict, current_cost, current_type_name)


def _print_types_dict(alloc_dict):
    print "----------------------------------------"
    all_types = alloc_dict["types"]
    print "Types:"
    for curr_type_name, current_type_obj in all_types.items():
        print "  {0}:{1}".format(curr_type_name, current_type_obj["cost"])

        print "    Users:"
        for curr_type_user_name, current_type_user_obj in current_type_obj["users"].items():
            print "      {0}:{1}".format(curr_type_user_name, current_type_user_obj)
        print "    Tenants:"
        for curr_type_tenant_name, current_type_tenant in current_type_obj["tenants"].items():
            print "      {0}:{1}".format(curr_type_tenant_name, current_type_tenant)


def _print_tenants_dict(alloc_dict):
    print "----------------------------------------"
    all_tenants = alloc_dict["tenants"]
    print "Tenants:"
    for curr_tenant_name, current_tenant_obj in all_tenants.items():
        print "  {0}:{1}".format(curr_tenant_name, current_tenant_obj["cost"])

        print "    Users:"
        for curr_tenant_user_name, current_tenant_user_obj in current_tenant_obj["users"].items():
            print "      {0}:{1}".format(curr_tenant_user_name, current_tenant_user_obj)
        print "    types:"
        for curr_tenant_type_name, current_type_cost in current_tenant_obj["types"].items():
            print "      {0}:{1}".format(curr_tenant_type_name, current_type_cost)


def _print_groups_dict(alloc_dict):
    print "----------------------------------------"
    all_groups = alloc_dict["groups"]
    print "Groups:"
    for curr_group_name, current_group_obj in all_groups.items():
        print "  {0}:{1}".format(curr_group_name, current_group_obj["cost"])

        print "    Users:"
        for curr_group_user_name, current_group_user_obj in current_group_obj["users"].items():
            print "      {0}:{1}".format(curr_group_user_name, current_group_user_obj)
        print "    types:"
        for curr_group_type, group_type_cost in current_group_obj["types"].items():
            print "      {0}:{1}".format(curr_group_type, group_type_cost)


def _print_users_dict(alloc_dict):
    print "----------------------------------------"
    all_types = alloc_dict["users"]
    print "Users:"
    for curr_user_name, current_user_obj in all_types.items():
        print "  {0}:{1}".format(curr_user_name, current_user_obj["cost"])
        print "    types:"
        for curr_user_type, group_user_type_cost in current_user_obj["types"].items():
            print "      {0}:{1}".format(curr_user_type, group_user_type_cost)


class CostView(generic.ListView):
    template_name = 'rms/cost.html'
    context_object_name = 'cost_dict'

    def get_queryset(self):
        """Return the last five allocated resources."""
        allocation_count = AllocatedResources.objects.count()
        alloc_dict = _init_alloc_dict(allocation_count)

        allocations = AllocatedResources.objects.order_by('allocation_time')[::-1]
        for alloc in allocations:
            _update_alloc_dict(alloc, alloc_dict)

        #_print_types_dict(alloc_dict)
        #_print_tenants_dict(alloc_dict)
        #_print_groups_dict(alloc_dict)
        #_print_users_dict(alloc_dict)

        return alloc_dict


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