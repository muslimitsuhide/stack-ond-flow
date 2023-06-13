from . import models
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import *
from django.http import Http404

def paginate(objects_list, request, per_page=3):
    paginator = Paginator(objects_list, per_page)
    try:
        limit = int(request.GET.get('page', 10))
    except ValueError:
        limit = 10
    if limit > 10:
        limit = 10
    try:
        page_number  = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    return paginator.get_page(page_number)

def index(request):
    questions = models.QUESTIONS
    page_obj = paginate(questions, request, 3)
    context = {'page_obj': page_obj,
               'questions': models.QUESTIONS,
               'tags': models.TAGS,
               'users': models.USER,}
    return render(request, 'index.html', context)

def question(request, question_id: int):
    try:
        questions = models.QUESTIONS
        answers = models.ANSWERS

        page_obj = paginate(answers, request, 3)
        question = questions[question_id]

        context = {'page_obj': page_obj,
                'question': question,
                'answers': answers,
                'tags': models.TAGS,
                'users': models.USER}
    except:
        raise Http404("Question does not exist")
    
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
    try:
        tags = models.TAGS
        page_obj = paginate(tags, request, 3)
        tag = tags[tag_id]

        questions_with_tag = []
        for question in models.QUESTIONS:
            for _tag in question['tags']:
                if _tag['id'] == tag_id:
                    questions_with_tag.append(question)

        p = Paginator(questions_with_tag, 10)

        questions = p.get_page(page_num)

        context = {'page_obj': page_obj,
                'tag': tag,
                'questions': questions,
                'tags': models.TAGS,
                'users': models.USER}
    
    except:
         raise Http404("Tag does not exist")

    return render(request, 'tag.html', context)
