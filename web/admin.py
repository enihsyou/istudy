from django.contrib import admin
from django.contrib.admin.options import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User, Group

from web import models

from web.models import Student, Course, Paper, Question, Lesson, Teacher, TakeCourse

admin.site.site_header = "项目管理课程系统"


admin.site.unregister(Group)


@admin.register(Student)
class StudentUserAdmin(admin.ModelAdmin):
    class TakeInline(admin.StackedInline):
        model = TakeCourse
        readonly_fields = ('final_term_grade',)
        fieldsets = (
            (None, {'fields': ('course.name', )}),
            ('分数', {'fields': ('usual_behave_grade', 'master_test_grade', 'final_term_grade')}),
        )
        extra = 0

    fields = ('name', 'password')

    list_display = ('name', 'add_time', 'take_course_count')
    inlines = (TakeInline,)


@admin.register(Teacher)
class TeacherUserAdmin(admin.ModelAdmin):
    class CourseInline(admin.StackedInline):
        model = Course
        extra = 0

    fields = ('name', 'password')
    fieldsets = ()
    list_display = ('name', 'add_time', 'teaching_course_count')
    inlines = (CourseInline,)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    class LessonAdminInline(admin.TabularInline):
        model = Lesson
        extra = 0

    inlines = (LessonAdminInline,)
    list_display = ('name', 'teacher', 'add_time', 'student_count', 'lesson_count')


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    class QuestionInline(admin.TabularInline):
        model = Question
        extra = 0

    inlines = (QuestionInline,)
    list_display = ('title', 'create_time', 'question_count')
