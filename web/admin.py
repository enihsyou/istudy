from django.contrib import admin
from django.contrib.admin.options import *

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from web import models
#
# admin.site.register(models.Student)
# admin.site.register(models.TakeCourse)
#
#
# class TeacherAdmin(admin.ModelAdmin):
#     pass
#
#
# class PaperAdmin(admin.ModelAdmin):
#     class QuestionInline(admin.TabularInline):
#         model = models.Question
#
#     inlines = [QuestionInline]
#
#
# # 最后进行全部的注册工作
# admin.site.register(Teacher, TeacherAdmin)
# admin.site.register(Paper, PaperAdmin)
from web.models import Student, Course, Paper, Question, Lesson, Teacher


@admin.register(Student)
class StudentUserAdmin(admin.ModelAdmin):
    fields = ('name', 'password')
    list_display = ('name', 'add_time')


# admin.site.register(Student, StudentUserAdmin)


# admin.site.register(Student, StudentUserAdmin)

@admin.register(Teacher)
class TeacherUserAdmin(admin.ModelAdmin):
    fields = ('name', 'password')
    list_display = ('name', 'add_time')


# admin.site.register(Teacher, TeacherUserAdmin)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    class LessonAdminInline(admin.TabularInline):
        model = Lesson
        extra = 2

    inlines = (LessonAdminInline,)
    list_display = ('name', 'teacher', 'add_time')


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    class QuestionInline(admin.TabularInline):
        model = Question
        extra = 1

    inlines = (QuestionInline,)
    list_display = ('title', 'create_time', 'question_count')
