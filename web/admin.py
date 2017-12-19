from django.contrib import admin
from django.contrib.admin.options import *

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User, Group

from web import models

from web.models import Student, Course, Paper, Question, Lesson, Teacher, TakeCourse, MyUser

admin.site.site_header = "项目管理课程系统"


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name', 'add_time')

    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ()
    list_filter = ('is_admin',)


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)


@admin.register(Student)
class StudentUserAdmin(admin.ModelAdmin):
    class TakeInline(admin.StackedInline):
        model = TakeCourse
        readonly_fields = ('final_term_grade',)
        fields = ('usual_behave_grade', 'master_test_grade', 'final_term_grade')
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
