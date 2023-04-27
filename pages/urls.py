from django.urls import path

from . import views

urlpatterns = [
    path('', views.intro_view, name='intro'),
    path('home/', views.home_view, name='home'),
    path('login/', views.login_user_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('level/', views.level_view, name='level'),
    path('lessons/manage', views.lesson_manage_view, name='lesson_manage'),
    path('lessons/add', views.lesson_add_view, name='lesson_add'),
    path('lesson/edit/<int:lesson_id>', views.lesson_edit_view, name='lesson_edit'),
    path('lesson/delete/<int:lesson_id>', views.lesson_delete, name='lesson_delete'),
    path('lessons/<int:level_id>/', views.lesson_view, name='lesson'),
    path('lessons/finished/<int:lesson_id>/', views.lesson_finished, name='lesson_finished'),
    path('lesson/<int:lesson_id>/', views.lesson_single_view, name='lesson_single'),
    path('levels/manage', views.level_manage_view, name='level_manage'),
    path('levels/add', views.level_add_view, name='level_add'),
    path('level/edit/<int:level_id>', views.level_edit_view, name='level_edit'),
    path('level/delete/<int:level_id>', views.level_delete, name='level_delete'),
    path('activity/<int:lesson_id>/', views.difficulty_view, name='difficulty'),
    path('activity/<int:lesson_id>/<str:difficulty>/', views.activity_view, name='activity'),
    path('activity/add/<int:lesson_id>', views.activity_add_view, name='activity_add'),
    path('activity/edit/<int:activity_id>', views.activity_edit_view, name='activity_edit'),
    path('activity/delete/<int:activity_id>', views.activity_delete, name='activity_delete'),
    path('activity/review/<int:user_id>/<int:activity_id>', views.activity_review, name='activity_review'),
    path('question/<int:activity_id>/', views.question_view, name='question'),
    path('question/add/<int:activity_id>', views.question_add_view, name='question_add'),
    path('question/edit/<int:question_id>', views.question_edit_view, name='question_edit'),
    path('question/delete/<int:question_id>', views.question_delete, name='question_delete'),
    path('answer/add/<int:question_id>', views.answer_add_view, name='answer_add'),
    path('answer/edit/<int:answer_id>', views.answer_edit_view, name='answer_edit'),
    path('answer/delete/<int:answer_id>', views.answer_delete, name='answer_delete'),
    path('user/profile/<int:user_id>', views.user_profile, name='user_profile'),
    path('user/admin', views.admin_view, name='admin'),
    path('user/manage', views.user_manage, name='user_manage'),
    path('user/add', views.user_add_view, name='user_add'),
    path('user/edit/<int:user_id>', views.user_edit_view, name='user_edit'),
    path('user/password/change/<int:user_id>', views.change_password_view, name='user_change_password'),
    path('user/password/reset/<int:user_id>', views.reset_password, name='user_reset_password'),
    path('user/delete/<int:user_id>', views.user_delete, name='user_delete'),
    path('retrieve', views.retrieve_view, name='retrieve'),
    path('retrieve/lessons', views.retrieve_lessons_view, name='retrieve_lessons'),
    path('retrieve/lesson/<int:lesson_id>', views.retrieve_lesson, name='retrieve_lesson'),
    path('retrieve/activities', views.retrieve_activities_view, name='retrieve_activities'),
    path('retrieve/activity/<int:activity_id>', views.retrieve_activity, name='retrieve_activity'),
    path('retrieve/questions', views.retrieve_questions_view, name='retrieve_questions'),
    path('retrieve/question/<int:question_id>', views.retrieve_question, name='retrieve_question'),
    path('retrieve/answers', views.retrieve_answers_view, name='retrieve_answers'),
    path('retrieve/answer/<int:answer_id>', views.retrieve_answer, name='retrieve_answer'),
]
