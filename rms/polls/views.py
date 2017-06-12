# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import loader
from django.http import Http404
from .models import Choice, Question

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic


# Create your views here.


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


#def detail(request, question_id):
#    return HttpResponse("You're looking at question %s." % question_id)

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        #raise Http404("Question does not exist")
        return render(request, 'polls/no_such_question.html', {'question_id': question_id})
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice = request.POST.get('choice')

    if choice:
        question.choice_set.create(choice_text=choice, votes=0)
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
    else:
        render_ctx = {
            'question': question
        }
        if request.POST.get('after_first_load'):
            render_ctx['error_message'] = "Choice text is empty."

    return render(request, 'polls/add_choice.html', render_ctx)


def delete_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    choice_id = request.POST.get('choice_id')
    if choice_id:
        current_choice = question.choice_set.get(pk=choice_id)
        current_choice.delete()
        return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
    else:
        render_ctx = {
            'question': question
        }

        if request.POST.get('after_first_load'):
            render_ctx['error_message'] = "You didn't select a choice to delete"

    return render(request, 'polls/delete_choice.html', render_ctx)

