from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms

from accounts.models import User
from pages.models import Lesson, Activity, Question, Answer, Level


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class LessonForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())  # Use the RichTextField widget

    class Meta:
        model = Lesson
        fields = ('title', 'description', 'level')


class LevelForm(forms.ModelForm):

    class Meta:
        model = Level
        fields = ('name',)


class ActivityForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Activity
        fields = ['title', 'description', 'difficulty']


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['name']


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['name', 'is_correct']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'contact_no', 'is_admin']


class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['old_password', 'password1', 'password2',]

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('password1')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'old_password', 'password1', 'password2', 'first_name', 'middle_name', 'last_name', 'email', 'contact_no']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'})
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('password1')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user
