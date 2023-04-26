from . import models
from django.shortcuts import render


def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context)

def question(request):
    return render(request, 'question.html')

def login(request):
    return render(request, 'login.html')

def ask(request):
    return render(request, 'ask.html')
