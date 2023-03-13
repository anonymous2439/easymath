from django.contrib import admin

from .models import Activity, Lesson, Question, Answer, Level, UserAnswer, FinishedLesson

# Register your models here.
admin.site.register(Activity)
admin.site.register(Lesson)
admin.site.register(FinishedLesson)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Level)
admin.site.register(UserAnswer)
