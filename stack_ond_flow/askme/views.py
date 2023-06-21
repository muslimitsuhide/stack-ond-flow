from django.contrib.auth.decorators import login_required
from django.db.models.fields import json
import json
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.core.paginator import Paginator
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods, require_POST
from . import models
from .forms import *
from pack_ajax.ajax import login_required_ajax, HttpResponseAjax, HttpResponseAjaxError

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


def question(request, question_id):
    question = models.Question.objects.get_question(question_id)
    if question == None:
        raise Http404("Question does not exist")
    answers = models.Answer.objects.get_by_question(question_id)
    page_obj = paginate(answers, request, 3)
    context = {'question': question, 'page_obj':page_obj}
    sidebar_content(context)
    if request.method == "GET":
        answer_form = AnswerForm()
    elif request.method == "POST":
        if request.user.is_anonymous:
            return HttpResponseRedirect(reverse("login"))
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer_id = answer_form.save(request.user, question)
            answers_cnt = question.answers.count()
            num_page = (answers_cnt // 10) + 1
            return HttpResponseRedirect(reverse("question", args=[question_id]) + f"?page=1#answer-{answer_id}")
    context['form'] = answer_form
    return render(request, "question.html", context)


@csrf_protect
def login(request):
    context = {}
    sidebar_content(context)
    if request.method == 'GET':
        login_form = LoginForm()
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                continue_url = request.GET.get("continue")
                if continue_url is None or continue_url[0] != "/":
                    continue_url = "/"
                return HttpResponseRedirect(continue_url)
            else:
                login_form.add_error(field=None, error="Wrong username or/and password")
    context['form'] = login_form
    return render(request, "login.html", context)


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


@csrf_protect
def register(request):
    context = {}
    sidebar_content(context)
    if request.method == 'GET':
        reg_form = RegistrationForm()
    elif request.method == 'POST':
        reg_form = RegistrationForm(request.POST, request.FILES)
        if reg_form.is_valid():
            reg_form.save()
            user = auth.authenticate(request=request, **reg_form.cleaned_data)
            if user:
                auth.login(request, user)
                continue_url = request.GET.get('continue')
                if continue_url is None or continue_url[0] != '/':
                    continue_url = '/'
                return HttpResponseRedirect(continue_url)
            else:
                reg_form.add_error(field=None, error='Wrong username or password')
    context['form'] = reg_form
    return render(request, 'register.html', context)


@login_required(login_url='login')
def profile_edit(request):
    context = {}
    sidebar_content(context)
    if request.method == 'GET':
        edit_form = ProfileEditForm(request.user)
    elif request.method == 'POST':
        edit_form = ProfileEditForm(request.user, request.POST, request.FILES)
        if edit_form.is_valid():
            edit_form.save()
    context['form'] = edit_form
    return render(request, 'edit.html', context)


@login_required(login_url='login', redirect_field_name='continue')
def ask(request):
    context = {}
    sidebar_content(context)
    if request.method == 'GET':
        ask_form = QuestionForm()
    elif request.method == 'POST':
        ask_form = QuestionForm(request.POST)
        if ask_form.is_valid():
            question_id = ask_form.save(request.user)
            return HttpResponseRedirect(reverse('question', args=[question_id]))
    context['form'] = ask_form
    return render(request, 'ask.html', context)


def tag(request, tag):
    try:
        questions = models.Question.objects.tag_questions(models.Tag.objects.get_by_title(tag))
        page_obj = paginate(questions, request, 3)
        context = {'page_obj': page_obj, 'title': f'Tag:{tag} Questions'}
        sidebar_content(context)

    except:
         raise Http404('Tag does not exist')

    return render(request, 'index.html', context)


@login_required_ajax
@require_POST
def vote(request):
    data = json.loads(request.body)
    question_id = data["question_id"]
    type_of_vote = data["vote"]
    new_rating = models.Like.objects.set_like(question_id, request.user.id, type_of_vote)
    if new_rating is None:
        return HttpResponseAjaxError(code="not_exist", message="Question or/ans user doesnt exist")
    return HttpResponseAjax(new_rating=new_rating)


@login_required_ajax
@require_POST
def correct(request):
    data = json.loads(request.body)
    answer_id = data["answer_id"]
    question_id = data["question_id"]
    if request.user != models.Question.objects.get(pk=question_id).author.user:
        return HttpResponseAjaxError(code="not_user", message="Not proper user")
    models.Answer.objects.set_correct(answer_id)
    return HttpResponseAjax()
