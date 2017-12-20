# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.urls import path, include

from web import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.logout, name='logout'),
    path('course/', include([
        path('list/', views.CourseListView.as_view(), name='course_list'),
        path('<int:course>/', views.CourseDetailView.as_view(), name='course_detail'),
        path('<int:course>/<int:lesson>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    ])),
    path('paper/', include([
        path('list/', views.PaperListView.as_view(), name='paper_list'),
        path('add/', views.paper_create_view, name='paper_create'),
        path('<int:pk>/', views.PaperDetailView.as_view(), name='paper_detail'),
    ])),
    path('student/', include([
        path('signup/', views.student_signup_view, name='student_create'),
        path('login/', views.student_login_view, name='student_login'),
        path('<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
        path('<int:pk>/edit', views.StudentUpdateView.as_view(), name='student_edit'),
        path('<int:pk>/delete', views.StudentDeleteView.as_view(), name='student_delete'),
        path('<int:student>/course/', include([
            path('list/', views.StudentCourseListView.as_view(), name='student_course_list'),
            path('list/all', views.StudentCourseListAllView.as_view(), name='student_course_list_all'),
            path('<int:course>/join/', views.course_join_view, name='student_join_course')
        ]))
    ])),
    path('teacher/', include([
        path('signup/', views.teacher_signup_view, name='teacher_create'),
        path('login/', views.teacher_login_view, name='teacher_login'),
        path('<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
        path('<int:pk>/edit', views.TeacherUpdateView.as_view(), name='teacher_edit'),
        path('<int:pk>/delete', views.TeacherDeleteView.as_view(), name='teacher_delete'),
        path('<int:teacher>/course/', include([
            path('list/', views.TeacherCourseListView.as_view(), name='teacher_course_list'),
            path('new/', views.CourseCreateView.as_view(), name='teacher_course_create'),
            path('<int:course>/', views.CourseDetailView.as_view(), name='course_detail'),
            path('<int:course>/add_lesson', views.TeacherLessonCreateView.as_view(), name='teacher_lesson_create'),
            path('<int:course>/edit', views.TeacherCourseUpdateView.as_view(), name='course_edit'),
            path('<int:course>/delete', views.TeacherCourseDeleteView.as_view(), name='course_delete'),
        ]))
    ])),
]
