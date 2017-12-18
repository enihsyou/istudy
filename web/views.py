from django.contrib.auth.views import LogoutView, LoginView, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.base import *

from web.form import *
from web.models import *


class IndexView(TemplateView):
    template_name = "index.html"


# 课程操作视图

class CourseListView(ListView):
    """列出所有相关课程"""
    model = Course
    template_name = "course_list.html"


class CourseCreateView(CreateView):
    """教师添加自己教学的课程"""
    model = Course
    fields = ['name', 'detail']
    template_name = "course_create.html"
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        detail = form.cleaned_data['detail']
        teacher_id = 9
        Course(teacher=teacher_id, name=name, detail=detail).save()
        return redirect(self.get_success_url())


class CourseUpdateView(UpdateView):
    """教师更新课程信息"""
    model = Course
    template_name = "course_update.html"
    fields = ['name', 'detail']
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        detail = form.cleaned_data['detail']
        teacher_id = 9
        course = Course.objects.get(teacher=teacher_id, name=name)
        course.name = name
        course.detail = detail
        course.save()
        return redirect(self.get_success_url())


class CourseDeleteView(DeleteView):
    """教师删除课程"""
    model = Course
    success_url = reverse_lazy('course_list')
    template_name = "course_delete.html"


class LessonListView(ListView):
    """列出课程里全部的教学章节，右边是学习（下载）链接"""
    model = Lesson
    template_name = "lesson_list.html"


# 学生操作视图

class StudentLoginView(LoginView):
    """学生登陆"""
    template_name = "student_login.html"
    form_class = StudentLoginForm
    success_url = reverse_lazy("student_detail")

    def form_valid(self, form):
        name = form.cleaned_data["username"]
        password = form.cleaned_data['password']
        remember_me = form.cleaned_data['remember_me']
        student = Student.objects.get(name=name)
        if student.password == password:
            login(student)
            return redirect(self.get_success_url())


class StudentCreateView(CreateView):
    """学生注册"""
    form_class = StudentCreateForm
    template_name = "student_signup.html"
    success_url = reverse_lazy("student_login")

    def form_valid(self, form):
        name = form.cleaned_data["username"]
        password = form.cleaned_data['password']
        Student(name=name, password=password).save()
        return redirect(self.success_url)

    class Meta:
        model = Student
        fields = ("name",)
        field_classes = {'name': UsernameField}


class StudentLogoutView(TemplateView):
    template_name = "student_logout.html"


class StudentDetailView(DetailView):
    """展示学生个人信息"""
    model = Student
    template_name = "student_detail.html"


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'student_update.html'
    fields = ['name', 'detail']
    success_url = reverse_lazy('student_detail.html')


class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('student_login')


# Student Course
class StudentJoinCourseView(CreateView):
    pass


# Student Exam
class StudentTakeExam(View):
    pass


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
    template_name = "teacher_update.html"
    fields = ['name', 'detail']
    success_url = reverse_lazy('teacher_detail')


class TeacherDeleteView(DeleteView):
    model = Teacher
    success_url = reverse_lazy('teacher_login')


# PaperView
class PaperListView(ListView):
    model = Paper
    template_name = "paper_list.html"


class PaperCreateView(CreateView):
    model = Paper
    template_name = "paper_create.html"
    forms = PaperCreateForm
