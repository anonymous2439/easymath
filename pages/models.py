from django.db import models
from ckeditor.fields import RichTextField

from accounts.models import User

difficulties = (
    ('easy', 'EASY MODE'),
    ('medium', 'MEDIUM MODE'),
    ('hard', 'HARD MODE'),
)


class Level(models.Model):
    name = models.CharField(max_length=30)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=50)
    description = RichTextField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class FinishedLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lesson', 'user'], name='lesson_user'
            )
        ]


class Activity(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20, choices=difficulties, default='easy')
    date_created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'activity'
        verbose_name_plural = 'activities'


class SubmittedActivity(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.submitted_by)+' - '+str(self.activity)

    class Meta:
        verbose_name = 'SubmittedActivity'
        verbose_name_plural = 'SubmittedActivities'
        unique_together = ('activity', 'submitted_by',)


class Question(models.Model):
    name = RichTextField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Answer(models.Model):
    name = models.CharField(max_length=50)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)+' - '+str(self.answer)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'answer'], name='user_answer'
            )
        ]
