from django.urls import path

from . import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('home/', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('lesson/', views.lesson, name='lesson'),
    path('activity/<int:lesson_id>/', views.activity, name='activity'),
    path('question/<int:activity_id>/', views.question, name='question'),
]