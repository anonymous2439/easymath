from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import User
from .forms import LoginForm
from .models import Lesson, Activity


def intro(request):
    template = 'pages/intro.html'
    return render(request, template, {"is_intro": True})


def home(request):
    template = 'pages/home.html'
    return render(request, template)


def login_user(request):
    template = 'pages/login.html'
    # GET THE LOGIN FORM VALUES IF REQUEST IS POST
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        # INITIALIZE LOGIN FORM FOR THE TEMPLATE
        login_form = LoginForm()
        # GI FLAG LANG NI AS "is_intro" PARA DILI MU SHOW ANG LEFT NAV SA LOGIN PAGE
    return render(request, template, {"login_form": login_form, "is_intro": True})


def lesson(request):
    template = 'pages/lesson.html'
    lessons = Lesson.objects.all()
    context = {"lessons": lessons}
    return render(request, template, context)


def activity(request, lesson_id):
    template = 'pages/activity.html'
    activities = Lesson.objects.get(pk=lesson_id).activity_set.all()
    context = {'activities': activities}
    return render(request, template, context)


def question(request, activity_id):
    template = 'pages/question.html'
    questions = Activity.objects.get(pk=activity_id).question_set.all()
    context = {'questions': questions}
    return render(request, template, context)
