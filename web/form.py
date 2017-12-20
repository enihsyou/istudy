# -*- coding: UTF-8 -*-
from django import forms

from django.contrib.auth.forms import UserChangeForm, UserCreationForm, UsernameField, AuthenticationForm
from rolepermissions import roles
from rolepermissions.roles import assign_role

from web.models import Student, Teacher


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
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        assign_role(user, 'StudentRole')
        if commit:
            user.save()
        return user

    class Meta:
        model = Student
        fields = ("name",)
        field_classes = {'name': UsernameField}


class TeacherCreateForm(UserCreationForm):
    """老师注册"""

    # form_class = StudentSignupForm
    # template_name = "student_signup.html"
    # success_url = reverse_lazy("student_login")
    #
    # def form_valid(self, form):
    #     name = form.cleaned_data["username"]
    #     password = form.cleaned_data['password']
    #     Student(name=name, password=password).save()
    #     return redirect(self.success_url)
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        assign_role(user, 'TeacherRole')

        if commit:
            user.save()
        return user

    class Meta:
        model = Teacher
        fields = ("name",)
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


class StudentAnswerQuestionForm(forms.Form):
    pass


class QuestionCreateForm(forms.ModelForm):
    pass
