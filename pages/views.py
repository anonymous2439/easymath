from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import User
from .forms import LoginForm


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
    return render(request, template)
