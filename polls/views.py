from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Questions, Choice

def index(request):
    latest_question_list = Questions.objects.order_by("-pub_date")[:5]
    return render(request, 'polls/index.html', {'latest_questions_list': latest_question_list})

def details(request, question_id):
    question = Questions.objects.get(pk=1)
    return render(request, 'polls/details.html', {'question': question})

def results(request, question_id):
    return HttpResponse(f"Yönlendirildiğiniz sorunun sonucu: {question_id}")

def vote(request, question_id):
    return HttpResponse(f"Oy verdiğiniz soru: {question_id}")
    