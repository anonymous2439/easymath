from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count, Q
from django.forms import formset_factory
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User
from .forms import LoginForm, LessonForm, ActivityForm
from .models import Lesson, Activity, Level, UserAnswer, Answer, FinishedLesson, SubmittedActivity
from django.utils.safestring import mark_safe

difficulties = (
    ('easy', 'EASY MODE'),
    ('medium', 'MEDIUM MODE'),
    ('hard', 'HARD MODE'),
)

ACTIVITY_CONSTRAINT_ERROR = 'You already have submitted this activity'
USER_ADD_SUCCESS = 'User added successfully'
USER_EDIT_SUCCESS = 'User has been updated'
USER_DELETE_SUCCESS = 'User has been deleted'


def validate_is_admin(user):
    if not user.is_admin:
        # User is not an admin, return a 403 Forbidden response
        return HttpResponseForbidden("You do not have permission to access this page.")


def intro_view(request):
    template = 'pages/intro.html'
    return render(request, template, {"is_intro": True})


@login_required
def home_view(request):
    template = 'pages/home.html'
    user = request.user
    activities_submitted = SubmittedActivity.objects.filter(submitted_by=user).values_list('activity_id', flat=True)
    score = UserAnswer.objects.filter(user=user, answer__is_correct=True, answer__question__activity__in=activities_submitted).count()
    total_answered_questions = UserAnswer.objects.filter(user=user, answer__question__activity__in=activities_submitted).count()
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


from .forms import UserForm

def user_manage(request):
    users = User.objects.all()
    context = {'users': users}
    template = 'pages/user_manage.html'
    return render(request, template, context)


def user_add_view(request):
    template = 'pages/user_add.html'

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, USER_ADD_SUCCESS)
            return redirect('user_manage')
    else:
        user_form = UserForm()

    context = {
        'user_form': user_form,
    }

    return render(request, template, context)


def user_edit_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, USER_EDIT_SUCCESS)
            return redirect('user_manage')
    else:
        user_form = UserForm(instance=user)

    template = 'pages/user_edit.html'
    context = {'user_form': user_form, 'user': user}
    return render(request, template, context)


def user_delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, USER_DELETE_SUCCESS)
    return redirect('user_manage')


def level_view(request):
    template = 'pages/level.html'
    levels = Level.objects.all()
    context = {"levels": levels}
    return render(request, template, context)


def lesson_view(request, level_id):
    template = 'pages/lesson.html'
    lessons = Level.objects.get(pk=level_id).lesson_set.all()
    search_text = request.GET.get('s')
    if search_text:
        lessons = lessons.filter(title__icontains=search_text)
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
    user = request.user
    activities = Lesson.objects.get(pk=lesson_id).activity_set.filter(difficulty=difficulty).annotate(
        submitted=Count('submittedactivity', filter=Q(submittedactivity__submitted_by=user))
    )
    search_text = request.GET.get('s')
    if search_text:
        activities = activities.filter(title__icontains=search_text)

    context = {'activities': activities, 'difficulty': difficulty}
    return render(request, template, context)


def question_view(request, activity_id):
    # maoh ni ang mu handle sa pag click sa radio button para ma save sa user_answer table
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        answer_id = request.POST.get('answer')
        answer = Answer.objects.get(pk=answer_id)
        # pag handle ni sa answer whether isave ang answer or iedit ra if ever mana nig answer nga question
        user_answer, created = UserAnswer.objects.get_or_create(user=request.user, answer__question=answer.question,
                                                                defaults={'answer': answer})
        if not created:
            user_answer.answer = answer
            user_answer.save()
        return JsonResponse({'success': True})

    # para ni sa pag submit sa activity
    elif request.method == 'POST':
        activity = Activity.objects.get(pk=request.POST.get('activity_id'))
        submitted_by = request.user
        # nag check ni for IntegrityError, para mahibaw an if naa nay na submit nga activity daan sa database or wala
        try:
            SubmittedActivity.objects.create(activity=activity, submitted_by=submitted_by)
            messages.success(request, "Successfully submitted the activity")
        except IntegrityError:
            messages.error(request, ACTIVITY_CONSTRAINT_ERROR)
            pass

    # naa diri ang pag get sa question with their respective answers then ipasa dayon sa template
    all_questions = Activity.objects.get(pk=activity_id).question_set.all()
    user_answers = UserAnswer.objects.filter(user=request.user)
    questions = []
    for question in all_questions:
        question_dict = {'question': question, 'answers': question.answer_set.all()}
        user_answer = user_answers.filter(answer__question=question).first()
        if user_answer:
            question_dict['user_answer'] = user_answer
        questions.append(question_dict)
    # ang reason ngano gipasa sad ang activity_id kay para inig submit sa activity later on, mahibaw an kung onsa nga activity ang gi submit
    context = {'questions': questions, 'activity_id': activity_id}
    return render(request, 'pages/question.html', context)


def admin_view(request):
    if not request.user.is_admin:
        # User is not an admin, return a 403 Forbidden response
        return HttpResponseForbidden("You do not have permission to access this page.")
    return render(request, 'pages/admin.html')


def lesson_manage_view(request):
    lessons = Lesson.objects.all()
    context = {
        'lessons': lessons,
    }
    return render(request, 'pages/lesson_manage.html', context)


def lesson_add_view(request):
    activity_form_set = formset_factory(ActivityForm)
    if request.method == 'POST':
        lesson_form = LessonForm(request.POST)
        activity_formset = activity_form_set(request.POST)
        if lesson_form.is_valid() and activity_formset.is_valid():
            lesson = lesson_form.save()
            for activity_form in activity_formset:
                if activity_form.cleaned_data:
                    activity = activity_form.save(commit=False)
                    activity.lesson = lesson
                    activity.save()
            return redirect('lesson_manage')
    else:
        lesson_form = LessonForm()
        activity_formset = activity_form_set()
    context = {
        'lesson_form': lesson_form,
        'activity_formset': activity_formset,
    }
    return render(request, 'pages/lesson_add.html', context)


def lesson_edit_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.method == 'POST':
        lesson_form = LessonForm(request.POST, instance=lesson)
        if lesson_form.is_valid():
            lesson_form.save()
            # Redirect to success page
    else:
        lesson_form = LessonForm(instance=lesson)
    context = {'lesson_form': lesson_form, 'lesson': lesson}
    return render(request, 'pages/lesson_edit.html', context)


def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    lesson.delete()
    return redirect('lesson_manage')

