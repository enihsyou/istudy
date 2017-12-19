# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.urls import path, include

from web import views

course_urls = [
    path('list/', views.CourseListView.as_view(), name='course_list'),
]
lesson_urls = [
    path('<int:course>/', views.LessonListView.as_view(), name='lesson_list'),
    path('<int:course>/<int:lesson>/', views.LessonDetailView.as_view(), name='lesson_detail'),
]
paper_urls = [
    path('list/', views.PaperListView.as_view(), name='paper_list'),
    path('<int:paper>/', views.PaperDetailView.as_view(), name='paper_detail'),
]
student_course_urls = [
    path('list/', views.CourseListView.as_view(), name='course_list'),
    path('<int:course>/join/', views.CourseJoinView.as_view(), name='student_join_course')
]
student_urls = [
    path('signup/', views.StudentCreateView.as_view(), name='student_create'),
    path('login/', views.StudentLoginView.as_view(), name='student_login'),
    path('<int:student>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('<int:student>/edit', views.StudentUpdateView.as_view(), name='student_edit'),
    path('<int:student>/delete', views.StudentDeleteView.as_view(), name='student_delete'),
    path('course/', include(student_course_urls))
]
teacher_course_urls = [
    path('list/', views.CourseListView.as_view(), name='course_list'),
    path('new/', views.CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/edit', views.CourseUpdateView.as_view(), name='course_edit'),
    path('<int:pk>/delete', views.CourseDeleteView.as_view(), name='course_delete'),
]
teacher_urls = [
    path('signup/', views.TeacherCreateView.as_view(), name='teacher_create'),
    path('login/', views.TeacherLoginView.as_view(), name='teacher_login'),
    path('<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('<int:pk>/edit', views.TeacherUpdateView.as_view(), name='teacher_edit'),
    path('<int:pk>/delete', views.TeacherDeleteView.as_view(), name='teacher_delete'),
    path('course/', include(teacher_course_urls))
]

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.logout, name='logout'),
    path('course/', include(course_urls)),
    path('lesson/', include(lesson_urls)),
    path('paper/', include(paper_urls)),
    path('student/', include(student_urls)),
    path('teacher/', include(teacher_urls)),
]
