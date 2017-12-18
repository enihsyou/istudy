# -*- coding: UTF-8 -*-
from django import forms

from django.contrib.auth.forms import UserChangeForm, UserCreationForm, UsernameField, AuthenticationForm
from django.forms import ModelForm

from web.models import Student


class StudentSignupForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class StudentCreateForm(UserCreationForm):
    """学生注册"""

    # form_class = StudentSignupForm
    # template_name = "student_signup.html"
    # success_url = reverse_lazy("student_login")
    #
    # def form_valid(self, form):
    #     name = form.cleaned_data["username"]
    #     password = form.cleaned_data['password']
    #     Student(name=name, password=password).save()
    #     return redirect(self.success_url)

    class Meta:
        model = Student
        fields = ("name", )
        field_classes = {'name': UsernameField}


class StudentLoginForm(AuthenticationForm):
    # name = forms.CharField()
    # password = forms.CharField(widget=forms.PasswordInput())
    # remember_me = forms.ChoiceField(widget=forms.CheckboxInput())
    pass


class StudentUpdateForm(UserChangeForm):
    pass


# class Meta:
#     model = Student
class CreateQuestionForm(forms.Form):
    pass


class PaperCreateForm(forms.Form):
    pass


class StudentAnswerQuestionForm(forms.Form): pass
