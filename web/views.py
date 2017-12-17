import django
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.base import *
from extra_views import *

from web.form import MessageForm, StudentSignupForm
from web.models import Student, Course, Teacher


class IndexView(TemplateView):
    template_name = "index.html"


# 课程操作视图

class CourseListView(ListView):
    model = Course


class CourseCreateView(CreateView):
    model = Course
    fields = ['name', 'detail']
    success_url = reverse_lazy('course_list')


class CourseUpdateView(UpdateView):
    model = Course
    template_name_suffix = '_update_form'
    fields = ['name', 'detail']
    success_url = reverse_lazy('course_list')


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('course_list')


# 学生操作视图

class StudentLoginView(LoginView):
    pass


class StudentLogoutView(LogoutView):
    pass


class StudentCreateView(CreateView):
    model = Student
    fields = ['name', 'password']
    # form_class = StudentSignupForm
    template_name = "student_signup.html"
    success_url = "student_login"

    def form_valid(self, form):
        pass


class StudentDetailView(DetailView):
    model = Student


class StudentUpdateView(UpdateView):
    model = Student
    template_name_suffix = '_update_form'
    fields = ['name', 'detail']
    success_url = reverse_lazy('student_detail')


class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('student_login')


# 教师操作视图

class TeacherLoginView(LoginView):
    pass


class TeacherLogoutView(LogoutView):
    pass


class TeacherCreateView(CreateView):
    model = Teacher
    template_name = "student_signup.html"
    # form_class = StudentSignupForm
    # fields = ['username', 'password']


class TeacherDetailView(DetailView):
    model = Teacher


class TeacherUpdateView(UpdateView):
    model = Teacher
    template_name_suffix = '_update_form'
    fields = ['name', 'detail']
    success_url = reverse_lazy('teacher_detail')


class TeacherDeleteView(DeleteView):
    model = Teacher
    success_url = reverse_lazy('teacher_login')
