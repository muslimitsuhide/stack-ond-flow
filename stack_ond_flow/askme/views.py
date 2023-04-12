from . import models
from django.shortcuts import render


def index(request):
    context = {'questions': QUESTIONS}
    return render(request, 'index.html', context)


def question(request):
    return render(request, 'question.html')
