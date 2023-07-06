from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Questions, Choice

def index(request):
    latest_question_list = Questions.objects.order_by("-pub_date")[:5]
    return render(request, 'polls/index.html', {'latest_questions_list': latest_question_list})

def details(request, question_id):
    question = Questions.objects.get(pk=question_id)
    return render(request, 'polls/details.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
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