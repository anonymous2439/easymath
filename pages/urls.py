from django.urls import path

from . import views

urlpatterns = [
    path('', views.intro_view, name='intro'),
    path('home/', views.home_view, name='home'),
    path('login/', views.login_user_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('level/', views.level_view, name='level'),
    path('lessons/<int:level_id>/', views.lesson_view, name='lesson'),
    path('lessons/finished/<int:lesson_id>/', views.lesson_finished, name='lesson_finished'),
    path('lesson/<int:lesson_id>/', views.lesson_single_view, name='lesson_single'),
    path('activity/<int:lesson_id>/', views.difficulty_view, name='difficulty'),
    path('activity/<int:lesson_id>/<str:difficulty>/', views.activity_view, name='activity'),
    path('activity/add/<int:lesson_id>', views.activity_add_view, name='activity_add'),
    path('activity/edit/<int:activity_id>', views.activity_edit_view, name='activity_edit'),
    path('question/<int:activity_id>/', views.question_view, name='question'),
    path('question/add/<int:activity_id>', views.question_add_view, name='question_add'),
    path('question/edit/<int:question_id>', views.question_edit_view, name='question_edit'),
    path('answer/add/<int:question_id>', views.answer_add_view, name='answer_add'),
    path('answer/edit/<int:answer_id>', views.answer_edit_view, name='answer_edit'),
    path('user/admin', views.admin_view, name='admin'),
    path('user/manage', views.user_manage, name='user_manage'),
    path('user/add', views.user_add_view, name='user_add'),
    path('user/edit/<int:user_id>', views.user_edit_view, name='user_edit'),
    path('user/delete/<int:user_id>', views.user_delete, name='user_delete'),
    path('lessons/manage', views.lesson_manage_view, name='lesson_manage'),
    path('lessons/add', views.lesson_add_view, name='lesson_add'),
    path('lesson/edit/<int:lesson_id>', views.lesson_edit_view, name='lesson_edit'),
    path('lesson/delete/<int:lesson_id>', views.lesson_delete, name='lesson_delete'),
]