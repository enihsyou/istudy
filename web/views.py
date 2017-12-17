import django
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView, login
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.base import *
from extra_views import *

from web.form import StudentSignupForm, StudentLoginForm
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
    template_name = "student_login.html"
    form_class = StudentLoginForm
    success_url = reverse_lazy("student_detail")

    def form_valid(self, form):
        name = form.cleaned_data['name']
        password = form.cleaned_data['password']
        remember_me = form.cleaned_data['remember_me']
        student = Student.objects.get(name=name)
        if student.password == password:
            login(student)
            return redirect(self.success_url)



class StudentCreateView(FormView):
    form_class = StudentSignupForm
    template_name = "student_signup.html"
    success_url = reverse_lazy("student_login")
    authenticate()
    def form_valid(self, form):
        name = form.cleaned_data['name']
        password = form.cleaned_data['password']
        Student(name=name, password=password).save()
        return redirect(self.success_url)


class StudentLogoutView(TemplateView):
    template_name = "student_logout.html"


class StudentDetailView(DetailView):
    model = Student


class StudentUpdateView(UpdateView):
    model = Student
    template_name_suffix = '_update_form'
    fields = ['name', 'detail']
    success_url = reverse_lazy('student_detail.html')


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
