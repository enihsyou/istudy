# -*- coding: UTF-8 -*-
from django import forms

from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm

from web.models import Student


class StudentSignupForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class StudentLoginForm(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.ChoiceField(widget=forms.CheckboxInput())


class StudentUpdateForm(UserChangeForm):
    pass
    # class Meta:
    #     model = Student
