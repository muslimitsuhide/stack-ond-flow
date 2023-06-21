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


def sidebar_content(context):
    context['top_tags'] = models.Tag.objects.get_top5()
    context['top_users'] = models.Profile.objects.get_top5()


def index(request):
    questions = models.Question.objects.new_questions()
    page_obj = paginate(questions, request, 3)
    context = {'page_obj': page_obj, 'title': 'New Questions'}
    sidebar_content(context)
    return render(request, 'index.html', context)


def question(request, question_id: int):
    try:
        question = models.Question.objects.get_question(question_id)
        answers = models.Answer.objects.get_by_question(question_id)

        page_obj = paginate(answers, request, 3)

        context = {'question': question, 'page_obj':page_obj}
        sidebar_content(context)
    except:
        raise Http404("Question does not exist")
    
    return render(request, 'question.html', context)


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def ask(request):
    return render(request, 'ask.html')


def tag(request, tag):
    try:
        questions = models.Question.objects.tag_questions(models.Tag.objects.get_by_title(tag))
        page_obj = paginate(questions, request, 3)
        context = {'page_obj': page_obj, 'title': f'Tag:{tag} Questions'}
        sidebar_content(context)

    except:
         raise Http404("Tag does not exist")

    return render(request, 'index.html', context)
