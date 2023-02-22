from django.contrib import admin

from .models import Activity, Lesson, Question, Answer

# Register your models here.
admin.site.register(Activity)
admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(Answer)
