from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms

from pages.models import Lesson, Activity


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class LessonForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())  # Use the RichTextField widget

    class Meta:
        model = Lesson
        fields = ('title', 'description', 'level')


class ActivityForm(forms.ModelForm):
    description = RichTextField()

    class Meta:
        model = Activity
        fields = ['title', 'description', 'difficulty']
