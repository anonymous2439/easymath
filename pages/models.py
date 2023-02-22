from django.db import models
from ckeditor.fields import RichTextField

class Lesson(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

class Activity(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'activity'
        verbose_name_plural = 'activities'

class Question(models.Model):
    name = RichTextField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    name = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
