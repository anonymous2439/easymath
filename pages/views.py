import calendar
import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count, Q, Case, When, IntegerField
from django.db.models.functions import ExtractMonth
from django.forms import formset_factory
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User
from .forms import LoginForm, LessonForm, ActivityForm, QuestionForm, AnswerForm, UserForm, UserEditForm, \
    ChangePasswordForm, LevelForm
from .models import Lesson, Activity, Level, UserAnswer, Answer, FinishedLesson, SubmittedActivity, Question
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


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    template = 'pages/home.html'
    user = request.user

    activities_submitted_id = SubmittedActivity.objects.filter(submitted_by=user).values_list('activity_id', flat=True)
    activities_submitted = SubmittedActivity.objects.filter(submitted_by=user)
    total_answered_questions = UserAnswer.objects.filter(user=user, answer__question__activity__in=activities_submitted_id).count()
    activity_scores = []

    # STORE THE SCORES WHERE THE SCORE DICTIONARY ID IS THE ACTIVITY ID
    for activity_submitted in activities_submitted:
        correct_answer = UserAnswer.objects.filter(user=user, answer__is_correct=True, answer__question__activity=activity_submitted.activity).count()
        total = activity_submitted.activity.question_set.count()
        score = {
            'correct_answer': correct_answer,
            'total': total
        }
        activity_scores.append({
            'activity': activity_submitted.activity,
            'score': score
        })

    context = {
        'total_answered_questions': total_answered_questions,
        'activities_submitted': activities_submitted,
        'activity_scores': activity_scores,
    }
    return render(request, template, context)


def logout_user(request):
    logout(request)
    return redirect('login')


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


def user_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    template = 'pages/user_profile.html'
    activities_submitted = SubmittedActivity.objects.filter(submitted_by=user)
    score = {}
    activity_scores = []

    # STORE THE SCORES WHERE THE SCORE DICTIONARY ID IS THE ACTIVITY ID
    for activity_submitted in activities_submitted:
        correct_answer = UserAnswer.objects.filter(user=user, answer__is_correct=True,
                                                   answer__question__activity=activity_submitted.activity).count()
        total = activity_submitted.activity.question_set.count()
        score = {
            'correct_answer': correct_answer,
            'total': total
        }
        activity_scores.append({
            'activity': activity_submitted.activity,
            'score': score
        })
    context = {
        'user': user,
        'activity_scores': activity_scores
    }
    return render(request, template, context)


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
            user = form.save(commit=False)
            user.username = user.first_name + '.' + user.last_name
            user.set_password(user.first_name + '.' + user.last_name)
            form.save()
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
    user_form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, USER_EDIT_SUCCESS)
    template = 'pages/user_edit.html'
    context = {'user_form': user_form, 'user': user}
    return render(request, template, context)


def change_password_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_form = ChangePasswordForm(instance=user)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, instance=user)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password1 = form.cleaned_data.get('password1')
            new_password2 = form.cleaned_data.get('password2')

            # check if old password is correct
            if not user.check_password(old_password):
                messages.error(request, 'Old password is incorrect')

            # check if new passwords match
            elif new_password1 != new_password2:
                messages.error(request, 'New passwords do not match')

            else:
                form.save()
                messages.success(request, USER_EDIT_SUCCESS)
                return redirect('login')
    template = 'pages/user_change_password.html'
    context = {'user_form': user_form, 'user': user}
    return render(request, template, context)


def reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    new_password = user.first_name + '.' + user.last_name
    user.set_password(new_password)
    user.save()
    messages.success(request, 'Password Reset Successfully!')
    return redirect('user_edit', user_id=user_id)


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
    lessons = Level.objects.get(pk=level_id).lesson_set.all().filter(is_deleted=False)
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
    lesson = Lesson.objects.get(pk=lesson_id)
    context = {"lesson": lesson, "difficulties": difficulties}
    return render(request, template, context)


def activity_view(request, lesson_id, difficulty):
    template = 'pages/activity.html'
    user = request.user
    activities = Lesson.objects.get(pk=lesson_id).activity_set.filter(difficulty=difficulty).annotate(
        submitted=Count('submittedactivity', filter=Q(submittedactivity__submitted_by=user))
    ).filter(is_deleted=False)
    search_text = request.GET.get('s')
    if search_text:
        activities = activities.filter(title__icontains=search_text)

    context = {'activities': activities, 'difficulty': difficulty, 'lesson_id': lesson_id}
    return render(request, template, context)


def activity_review(request, user_id, activity_id):
    # naa diri ang pag get sa question with their respective answers then ipasa dayon sa template
    all_questions = Activity.objects.get(pk=activity_id).question_set.all().filter(is_deleted=False)
    user = User.objects.get(pk=user_id)
    user_answers = UserAnswer.objects.filter(user=user)
    questions = []
    for question in all_questions:
        question_dict = {'question': question, 'answers': question.answer_set.all()}
        user_answer = user_answers.filter(answer__question=question).first()
        if user_answer:
            question_dict['user_answer'] = user_answer
        questions.append(question_dict)
    context = {
        'questions': questions,
        'user': user
    }
    template = 'pages/activity_review.html'
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
            return redirect('activity', lesson_id=activity.lesson.pk, difficulty=activity.difficulty)
        except IntegrityError:
            messages.error(request, ACTIVITY_CONSTRAINT_ERROR)
            pass

    # naa diri ang pag get sa question with their respective answers then ipasa dayon sa template
    all_questions = Activity.objects.get(pk=activity_id).question_set.all().filter(is_deleted=False)
    user_answers = UserAnswer.objects.filter(user=request.user)
    questions = []
    for question in all_questions:
        question_dict = {'question': question, 'answers': question.answer_set.all().filter(is_deleted=False)}
        user_answer = user_answers.filter(answer__question=question).first()
        if user_answer:
            question_dict['user_answer'] = user_answer
        questions.append(question_dict)
    # ang reason ngano gipasa sad ang activity_id kay para inig submit sa activity later on, mahibaw an kung onsa nga activity ang gi submit
    activity = Activity.objects.get(pk=activity_id)
    context = {'questions': questions, 'activity': activity}
    return render(request, 'pages/question.html', context)


def question_add_view(request, activity_id):
    activity = Activity.objects.get(pk=activity_id)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.activity = activity
            question.save()
            messages.success(request, 'New Question Added!')
            return redirect('question_edit', question_id=question.pk)
        else:
            messages.error(request, question_form.errors)
    else:
        question_form = QuestionForm()
    context = {
        'question_form': question_form,
        'activity': activity,
    }
    return render(request, 'pages/question_add.html', context)


def question_edit_view(request, question_id):
    question = Question.objects.get(pk=question_id)
    answers = question.answer_set.all().filter(is_deleted=False)
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question)
        if question_form.is_valid():
            question_form.save()
            messages.success(request, 'Question Saved!')
            return redirect('activity_edit', activity_id=question.activity.pk)
    else:
        question_form = QuestionForm(instance=question)
    context = {'question_form': question_form, 'question': question, 'answers': answers}
    return render(request, 'pages/question_edit.html', context)


def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.is_deleted = True
    question.save()
    messages.success(request, 'Question Deleted!')
    return redirect('activity_edit', activity_id=question.activity.pk)


def answer_add_view(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.save()
            messages.success(request, 'New Answer Added!')
            return redirect('question_edit', question_id=question_id)
        else:
            messages.error(request, answer_form.errors)
    else:
        answer_form = AnswerForm()
    context = {
        'answer_form': answer_form,
        'question': question,
    }
    return render(request, 'pages/answer_add.html', context)


def answer_edit_view(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST, instance=answer)
        if answer_form.is_valid():
            answer_form.save()
            messages.success(request, 'Answer Saved!')
            return redirect('question_edit', question_id=answer.question.pk)
    else:
        answer_form = AnswerForm(instance=answer)
    context = {'answer_form': answer_form, 'answer': answer}
    return render(request, 'pages/answer_edit.html', context)


def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.is_deleted = True
    answer.save()
    messages.success(request, 'Answer Deleted!')
    return redirect('question_edit', question_id=answer.question.pk)


def admin_view(request):
    if not request.user.is_admin:
        # User is not an admin, return a 403 Forbidden response
        return HttpResponseForbidden("You do not have permission to access this page.")
    return render(request, 'pages/admin.html')


def lesson_manage_view(request):
    lessons = Lesson.objects.filter(is_deleted=False)
    context = {
        'lessons': lessons,
    }
    return render(request, 'pages/lesson_manage.html', context)


def lesson_add_view(request):
    lesson = None
    if request.method == 'POST':
        lesson_form = LessonForm(request.POST)
        if lesson_form.is_valid():
            lesson = lesson_form.save()
            messages.success(request, 'New Lesson Added')
            return redirect('lesson_edit', lesson_id=lesson.pk)
        else:
            messages.error(request, lesson_form.errors)
    else:
        lesson_form = LessonForm()
    context = {
        'lesson_form': lesson_form,
    }
    if lesson is not None:
        context['lesson'] = lesson
    return render(request, 'pages/lesson_add.html', context)


def lesson_edit_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    activities = lesson.activity_set.all().filter(is_deleted=False)
    if request.method == 'POST':
        lesson_form = LessonForm(request.POST, instance=lesson)
        if lesson_form.is_valid():
            lesson_form.save()
            messages.success(request, 'Lesson Saved!')
            return redirect('lesson_manage')
    else:
        lesson_form = LessonForm(instance=lesson)
    context = {'lesson_form': lesson_form, 'lesson': lesson, 'activities': activities,}
    return render(request, 'pages/lesson_edit.html', context)


def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    lesson.is_deleted = True
    lesson.save()
    # lesson.delete()
    messages.success(request, 'Lesson Deleted!')
    return redirect('lesson_manage')


def level_manage_view(request):
    levels = Level.objects.filter(is_deleted=False)
    context = {
        'levels': levels,
    }
    return render(request, 'pages/level_manage.html', context)


def level_add_view(request):
    level = None
    if request.method == 'POST':
        level_form = LevelForm(request.POST)
        if level_form.is_valid():
            level = level_form.save()
            messages.success(request, 'New Level Added')
            return redirect('level_edit', level_id=level.pk)
        else:
            messages.error(request, level_form.errors)
    else:
        level_form = LevelForm()
    context = {
        'level_form': level_form,
    }
    if level is not None:
        context['level'] = level
    return render(request, 'pages/level_add.html', context)


def level_edit_view(request, level_id):
    level = get_object_or_404(Level, pk=level_id)
    if request.method == 'POST':
        level_form = LevelForm(request.POST, instance=level)
        if level_form.is_valid():
            level_form.save()
            messages.success(request, 'Level Saved!')
            return redirect('level_manage')
    else:
        level_form = LevelForm(instance=level)
    context = {'level_form': level_form, 'level': level}
    return render(request, 'pages/level_edit.html', context)


def level_delete(request, level_id):
    level = get_object_or_404(Level, pk=level_id)
    level.is_deleted = True
    level.save()
    messages.success(request, 'Level Deleted!')
    return redirect('level_manage')


def activity_add_view(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    if request.method == 'POST':
        activity_form = ActivityForm(request.POST)
        if activity_form.is_valid():
            activity = activity_form.save(commit=False)
            activity.lesson = lesson
            activity.save()
            messages.success(request, 'New Activity Added')
            return redirect('activity_edit', activity_id=activity.pk)
        else:
            messages.error(request, activity_form.errors)
    else:
        activity_form = ActivityForm()
    context = {
        'activity_form': activity_form,
        'lesson': lesson,
    }
    return render(request, 'pages/activity_add.html', context)


def activity_edit_view(request, activity_id):
    activity = Activity.objects.get(pk=activity_id)
    questions = activity.question_set.all().filter(is_deleted=False)
    if request.method == 'POST':
        activity_form = ActivityForm(request.POST, instance=activity)
        if activity_form.is_valid():
            activity_form.save()
            messages.success(request, 'Activity Saved')
            return redirect('lesson_edit', lesson_id=activity.lesson.pk)
    else:
        activity_form = ActivityForm(instance=activity)
    context = {'activity_form': activity_form, 'activity': activity, 'questions': questions}
    return render(request, 'pages/activity_edit.html', context)


def activity_delete(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.is_deleted = True
    activity.save()
    messages.success(request, 'Activity Deleted!')
    return redirect('lesson_edit', lesson_id=activity.lesson.pk)


def retrieve_view(request):
    template = 'pages/retrieve.html'
    return render(request, template)


def retrieve_lessons_view(request):
    template = 'pages/retrieve_lessons.html'
    lessons = Lesson.objects.filter(is_deleted=True)
    context = {
        'lessons': lessons
    }
    return render(request, template, context)


def retrieve_lesson(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    lesson.is_deleted = False
    lesson.save()
    messages.success(request, 'Lesson Retrieved')
    return redirect('retrieve_lessons')


def retrieve_activities_view(request):
    template = 'pages/retrieve_activities.html'
    activities = Activity.objects.filter(is_deleted=True)
    context = {
        'activities': activities
    }
    return render(request, template, context)


def retrieve_activity(request, activity_id):
    activity = Activity.objects.get(pk=activity_id)
    activity.is_deleted = False
    activity.save()
    messages.success(request, 'Activity Retrieved')
    return redirect('retrieve_activities')


def retrieve_questions_view(request):
    template = 'pages/retrieve_questions.html'
    questions = Question.objects.filter(is_deleted=True)
    context = {
        'questions': questions
    }
    return render(request, template, context)


def retrieve_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    question.is_deleted = False
    question.save()
    messages.success(request, 'Question Retrieved')
    return redirect('retrieve_questions')


def retrieve_answers_view(request):
    template = 'pages/retrieve_answers.html'
    answers = Answer.objects.filter(is_deleted=True)
    context = {
        'answers': answers
    }
    return render(request, template, context)


def retrieve_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    answer.is_deleted = False
    answer.save()
    messages.success(request, 'Answer Retrieved')
    return redirect('retrieve_answers')
