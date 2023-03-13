from django.urls import path

from . import views

urlpatterns = [
    path('', views.intro_view, name='intro'),
    path('home/', views.home_view, name='home'),
    path('login/', views.login_user_view, name='login'),
    path('level/', views.level_view, name='level'),
    path('lessons/<int:level_id>/', views.lesson_view, name='lesson'),
    path('lessons/finished/<int:lesson_id>/', views.lesson_finished, name='lesson_finished'),
    path('lesson/<int:lesson_id>/', views.lesson_single_view, name='lesson_single'),
    path('activity/<int:lesson_id>/', views.difficulty_view, name='difficulty'),
    path('activity/<int:lesson_id>/<str:difficulty>/', views.activity_view, name='activity'),
    path('question/<int:activity_id>/', views.question_view, name='question'),
]