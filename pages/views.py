from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import User
from .forms import LoginForm
from .models import Lesson, Activity, Level, UserAnswer, Answer, FinishedLesson

difficulties = (
    ('easy', 'EASY MODE'),
    ('medium', 'MEDIUM MODE'),
    ('hard', 'HARD MODE'),
)


def intro_view(request):
    template = 'pages/intro.html'
    return render(request, template, {"is_intro": True})


def home_view(request):
    template = 'pages/home.html'
    user = request.user
    score = UserAnswer.objects.filter(user=user, answer__is_correct=True).count()
    total_answered_questions = UserAnswer.objects.filter(user=user).count()
    context = {
        'score': score,
        'total_answered_questions': total_answered_questions,
    }
    return render(request, template, context)


def login_user_view(request):
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


def level_view(request):
    template = 'pages/level.html'
    levels = Level.objects.all()
    context = {"levels": levels}
    return render(request, template, context)


def lesson_view(request, level_id):
    template = 'pages/lesson.html'
    lessons = Level.objects.get(pk=level_id).lesson_set.all()
    context = {"lessons": lessons}
    return render(request, template, context)


def lesson_single_view(request, lesson_id):
    template = 'pages/lesson_single.html'
    lesson = Lesson.objects.get(pk=lesson_id)
    context = {"lesson": lesson}
    return render(request, template, context)


def lesson_finished(request, lesson_id):
    finished_lesson = FinishedLesson.objects.filter(user=request.user, lesson=Lesson.objects.get(pk=lesson_id))
    if finished_lesson.count() == 0:
        FinishedLesson(user=request.user, lesson=Lesson.objects.get(pk=lesson_id)).save()

    return redirect('difficulty', lesson_id=lesson_id)


def difficulty_view(request, lesson_id):
    template = 'pages/difficulty.html'
    context = {"lesson_id": lesson_id, "difficulties": difficulties}
    return render(request, template, context)


def activity_view(request, lesson_id, difficulty):
    template = 'pages/activity.html'
    activities = Lesson.objects.get(pk=lesson_id).activity_set.filter(difficulty=difficulty)
    context = {'activities': activities, 'difficulty': difficulty}
    return render(request, template, context)


def question_view(request, activity_id):
    template = 'pages/question.html'
    if request.POST:
        answer = Answer.objects.get(pk=request.POST.get('answer'))
        UserAnswer(user=request.user, answer=answer).save()
    questions = Activity.objects.get(pk=activity_id).question_set.all()
    user_answers = UserAnswer.objects.filter(user=request.user, answer__question__in=questions)
    print(user_answers)
    context = {'questions': questions, 'user_answers': user_answers}
    return render(request, template, context)
