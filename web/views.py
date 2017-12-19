from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout, LoginView, login
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST, require_GET
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


class TeacherCourseListView(ListView):
    """列出所有相关课程"""

    def get_queryset(self):
        return Course.objects.filter(teacher_id=self.kwargs['teacher'])

    template_name = "teacher_course_list.html"


class StudentCourseListView(ListView):
    """列出所有相关课程"""

    def get_queryset(self):
        return TakeCourse.objects.filter(student_id=self.kwargs['student'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudentCourseListView, self).get_context_data(**kwargs)
        context['student'] = Student.objects.get(id=self.kwargs['student'])
        return context

    context_object_name = "course_list"
    template_name = "student_course_list.html"


class StudentCourseListAllView(ListView):
    """列出所有相关课程"""
    model = Course

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudentCourseListAllView, self).get_context_data(**kwargs)
        context['student'] = Student.objects.get(id=self.kwargs['student'])
        return context

    context_object_name = "course_list"
    template_name = "student_course_list_all.html"


class CourseCreateView(CreateView):
    """教师添加自己教学的课程"""
    model = Course
    fields = ['teacher', 'name', 'detail']
    template_name = "course_create.html"
    success_url = reverse_lazy('course_list')
    #
    # def form_valid(self, form):
    #     name = form.cleaned_data['name']
    #     detail = form.cleaned_data['detail']
    #     teacher_id = 9
    #     Course(teacher=teacher_id, name=name, detail=detail).save()
    #     return redirect(self.get_success_url())


class TeacherCourseUpdateView(UpdateView):
    """教师更新课程信息"""
    model = Course
    pk_url_kwarg = 'course'
    template_name = "course_update.html"
    fields = ['name', 'detail']

    def get_success_url(self):
        return reverse_lazy('course_list', self.kwargs['course'])
    #
    # def form_valid(self, form):
    #     name = form.cleaned_data['name']
    #     detail = form.cleaned_data['detail']
    #     teacher_id = 9
    #     course = Course.objects.get(teacher=teacher_id, name=name)
    #     course.name = name
    #     course.detail = detail
    #     course.save()
    #     return redirect(self.get_success_url())


class TeacherCourseDeleteView(DeleteView):
    """教师删除课程"""
    model = Course
    pk_url_kwarg = 'course'

    def get_success_url(self):
        return reverse_lazy('teacher_course_list', self.kwargs['teacher'])

    template_name = "course_delete.html"


class CourseDetailView(DetailView):
    model = Course
    pk_url_kwarg = 'course'
    template_name = "course_detail.html"


@require_GET
def course_join_view(request, student, course):
    try:
        cou = Course.objects.get(id=course)
        stu = Student.objects.get(id=student)
    except Course.DoesNotExist:
        raise Http404("Course not exist")
    except Student.DoesNotExist:
        raise Http404("Student not exist")
    TakeCourse(student=stu, course=cou).save()
    return redirect(reverse_lazy('student_course_list', kwargs={'student':student}))


class LessonListView(ListView):
    """列出课程里全部的教学章节，右边是学习（下载）链接"""

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course'])

    template_name = "lesson_list.html"


class LessonDetailView(DetailView):
    pk_url_kwarg = 'lesson'

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course'])  # , id=self.kwargs['lesson'])

    template_name = "lesson_detail.html"


# 学生操作视图

class StudentLoginView(LoginView):
    """学生登陆"""
    template_name = "student_login.html"
    success_url = reverse_lazy('course_list')


class StudentCreateView(CreateView):
    """学生注册"""
    form_class = StudentCreateForm
    template_name = "student_signup.html"
    success_url = reverse_lazy("student_login")

    class Meta:
        model = Student
        fields = ("name",)
        field_classes = {'name': UsernameField}


class StudentLogoutView(TemplateView):
    template_name = "student_logout.html"


class StudentDetailView(DetailView):
    """展示学生个人信息"""
    model = Student
    template_name = "student_index.html"


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'student_update.html'
    fields = ['name', 'detail']
    success_url = reverse_lazy('student_index.html')


class StudentDeleteView(DeleteView):
    model = Student
    success_url = reverse_lazy('student_login')


# Student Exam
class StudentTakeExam(View):
    pass


# 教师操作视图

class TeacherLoginView(LoginView):
    pass


class TeacherCreateView(CreateView):
    model = Teacher
    template_name = "student_signup.html"
    # form_class = StudentSignupForm
    # fields = ['username', 'password']


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = "teacher_index.html"


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
    form_class = PaperCreateForm


class QuestionCreateView(CreateView):
    model = Question
    template_name = "question_create.html"
    form_class = QuestionCreateForm


class PaperDetailView(DetailView):
    model = Paper
    template_name = "paper_detail.html"
