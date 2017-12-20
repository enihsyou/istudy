from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout, LoginView
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import *
from django.views.generic.base import *
from rolepermissions.checkers import has_permission

from web import form
from web.form import *
from web.models import *


class IndexView(TemplateView):
    template_name = "index.html"


@require_POST
def student_login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse_lazy('student_detail',
                                                 kwargs={
                                                     'pk': Student.objects.get(user=user).id
                                                 }))
    return HttpResponseRedirect(reverse_lazy('index'))


@require_POST
def student_signup_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username, password=password)
    student = Student.objects.create(user=user, name=username)

    login(request, user)
    return HttpResponseRedirect(student.get_absolute_url())


@require_POST
def teacher_login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse_lazy('teacher_detail',
                                                 kwargs={
                                                     'pk': Teacher.objects.get(user=user).id
                                                 }))
    return HttpResponseRedirect(reverse_lazy('index'))


@require_POST
def teacher_signup_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = User.objects.create_user(username, password=password)
    teacher = Teacher.objects.create(user=user, name=username)

    login(request, user)
    return HttpResponseRedirect(reverse_lazy('teacher_detail',
                                             kwargs={'pk': teacher.id}))


# 课程操作视图

class CourseListView(ListView):
    """列出所有相关课程"""
    model = Course
    template_name = "course_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        if has_permission(self.request.user, 'edit_course'):
            return qs.filter(teacher_id=self.request.user.id)
        elif has_permission(self.request.user, 'join_course'):
            return qs.filter(takecourse__student_id=self.request.user.id)
        else:  # 匿名用户
            return qs

    def get_template_names(self):
        if has_permission(self.request.user, 'edit_course'):
            return "teacher_course_list.html"
        elif has_permission(self.request.user, 'join_course'):
            return "student_course_list.html"
        else:  # 匿名用户
            return "course_list.html"


class TeacherCourseListView(ListView):
    """列出所有相关课程"""
    model = Teacher

    def get_queryset(self):
        return Course.objects.filter(teacher_id=self.kwargs['teacher'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeacherCourseListView, self).get_context_data(**kwargs)
        context['teacher'] = Teacher.objects.get(id=self.kwargs['teacher'])
        return context

    context_object_name = "course_list"

    template_name = "teacher_course_list.html"


@require_GET
def course_list(request, course=None, teacher=None, student=None, **kwargs):
    if teacher is not None:
        query_set = Course.objects.filter(teacher_id=teacher)
        teacher_object = Teacher.objects.get(id=teacher)
        context = {
            'course_list': query_set,
            'teacher': teacher_object
        }
    elif student is not None:
        query_set = TakeCourse.objects.filter(student_id=student)
        student_object = Student.objects.get(id=student)
        context = {
            'course_list': query_set,
            'student': student_object
        }
    else:
        query_set = Course.objects.all()
        context = {
            'course_list': query_set,
        }
    return render(request, 'course_list.html', context)


@require_GET
def course_detail(request, course=None, teacher=None, student=None, **kwargs):
    query_set = Course.objects.get(course_id=course)

    if teacher is not None:
        teacher_object = Teacher.objects.get(id=teacher)
        context = {
            'course': query_set,
            'teacher': teacher_object
        }
    elif student is not None:
        student_object = Student.objects.get(id=student)
        context = {
            'course': query_set,
            'student': student_object
        }
    else:
        context = {
            'course': query_set,
        }
    return render(request, 'course_detail.html', context)


@require_GET
class TeacherCourseDetailView(DetailView):
    """列出所有相关课程"""
    model = Course
    pk_url_kwarg = 'course'

    #
    # def get_queryset(self):
    #     return Course.objects.filter(teacher_id=self.kwargs['teacher'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TeacherCourseDetailView, self).get_context_data(**kwargs)
        context['teacher'] = Teacher.objects.get(id=self.kwargs['teacher'])
        return context

    template_name = "teacher_course_detail.html"


class TeacherLessonCreateView(CreateView):
    """列出所有相关课程"""
    model = Lesson
    fields = ('course', 'name', 'learn_url')
    template_name = "lesson_create.html"


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

    def get_success_url(self):
        return reverse_lazy('teacher_course_list', kwargs={
            'teacher': self.kwargs['teacher'],
        })


class TeacherCourseUpdateView(UpdateView):
    """教师更新课程信息"""
    model = Course
    pk_url_kwarg = 'course'
    template_name = "course_update.html"
    fields = ['name', 'detail']

    def get_success_url(self):
        return reverse_lazy('teacher_course_list', kwargs={
            'teacher': self.kwargs['teacher'],
        })


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
    return redirect(reverse_lazy('student_course_list', kwargs={'student': student}))


class LessonListView(ListView):
    """列出课程里全部的教学章节，右边是学习（下载）链接"""

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course'])

    template_name = "lesson_list.html"


class LessonDetailView(DetailView):
    pk_url_kwarg = 'lesson'
    model = Lesson

    def get_queryset(self):
        return Lesson.objects.filter(course_id=self.kwargs['course'])  # , id=self.kwargs['lesson'])

    template_name = "lesson_detail.html"


# 学生操作视图


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PaperListView, self).get_context_data(**kwargs)
        context['teacher'] = Teacher.objects.get(user_id=self.request.user.id)
        return context


def paper_create_view(request):
    paper = Paper("某某试卷")
    inlineFormSet = inlineformset_factory(Paper, Question, fields=('title', 'comment', 'answer'))
    if request.method == "POST":
        formset = inlineFormSet(request.POST, request.FILES, instance=paper)
        if formset.is_valid():
            paper.save()
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return HttpResponseRedirect(paper.get_absolute_url())
    else:
        formset = inlineFormSet(instance=paper)
    return render(request, 'paper_create.html', {'formset': formset})


class QuestionCreateView(CreateView):
    model = Question
    template_name = "question_create.html"
    form_class = QuestionCreateForm


class PaperDetailView(DetailView):
    model = Paper
    template_name = "paper_detail.html"
