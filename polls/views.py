from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Questions, Choice

# Generic views
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions_list"

    def get_queryset(self):
        return Questions.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Questions
    template_name = "polls/details.html"

    def get_queryset(self):
        """
        Henüz yayınlanmamış `Questions`ları dahil etmez.
        """
        return Questions.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Questions
    template_name = "polls/results.html"


def index(request):
    latest_question_list = Questions.objects.order_by("-pub_date")[:5]
    return render(request, 'polls/index.html', {'latest_questions_list': latest_question_list})

def details(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, 'polls/details.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    if request.method == "POST":
        question = get_object_or_404(Questions, pk=question_id)

        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question':question,
                'error_message': 'You didn\'t select a choice.'
            })
        
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question_id, )))
    else:
        return HttpResponse("<h1>Method Not Allowed</h1>", status=405)