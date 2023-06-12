from . import models
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import *
from django.http import Http404

def paginate(request):
    objects = question.objects.all()
    items_per_page = 3
    paginator = Paginator(objects, items_per_page)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
    }
    return render(request, 'index.html', context)

def index(request, page_num = 1):
    context = {'questions': models.QUESTIONS,
               'tags': models.TAGS,
               'users': models.USER,
               'page_num': page_num,}
    return render(request, 'index.html', context)

def question(request, question_id: int):
    questions = models.QUESTIONS
    answers = models.ANSWERS

    question = questions[question_id]

    context = {'question': question,
               'answers': answers,
               'tags': models.TAGS,
               'users': models.USER}

    return render(request, 'question.html', context)

def login(request):
    context = {'questions': models.QUESTIONS,
               'tags': models.TAGS,
               'users': models.USER}
    return render(request, 'login.html', context)

def register(request):
    context = {'questions': models.QUESTIONS,
               'tags': models.TAGS,
               'users': models.USER}
    return render(request, 'register.html', context)

def ask(request):
    context = {'questions': models.QUESTIONS,
               'tags': models.TAGS,
               'users': models.USER}
    return render(request, 'ask.html', context)

def tag(request, tag_id: int, page_num = 1):
    tags = models.TAGS

    tag = tags[tag_id]

    questions_with_tag = []
    for question in models.QUESTIONS:
        for _tag in question["tags"]:
            if _tag["id"] == tag_id:
                questions_with_tag.append(question)

    p = Paginator(questions_with_tag, 10)

    questions = p.get_page(page_num)

    context = {"authenticated": True,
               "tag": tag,
               "questions": questions,
               "tags": models.TAGS,
               "users": models.USER}

    return render(request, "tag.html", context=context)
