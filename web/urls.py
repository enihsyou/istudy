# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.urls import path, include

from web import views

course_urls = [
    path('list/', views.CourseCreateView.as_view(), name='course_list'),
    path('new/<int:pk>', views.CourseCreateView.as_view(), name='course_create'),
    path('edit/<int:pk>', views.CourseUpdateView.as_view(), name='course_edit'),
    path('delete/<int:pk>', views.CourseDeleteView.as_view(), name='course_delete'),
]
student_urls = [
    path('signup/', views.StudentCreateView.as_view(), name='student_create'),
    path('login/', views.StudentLoginView.as_view(), name='student_login'),
    path('logout/', views.StudentLogoutView.as_view(), name='student_logout'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student_detail.html'),
    path('edit/<int:pk>', views.StudentUpdateView.as_view(), name='student_edit'),
    path('delete/<int:pk>', views.StudentDeleteView.as_view(), name='student_delete'),
]
teacher_urls = [
    path('signup/', views.TeacherCreateView.as_view(), name='teacher_create'),
    path('login/', views.TeacherLoginView.as_view(), name='teacher_login'),
    path('logout/', views.TeacherLogoutView.as_view(), name='teacher_logout'),
    path('<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('edit/<int:pk>', views.TeacherUpdateView.as_view(), name='teacher_edit'),
    path('delete/<int:pk>', views.TeacherDeleteView.as_view(), name='teacher_delete'),
]

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('course/', include(course_urls)),
    path('student/', include(student_urls)),
    path('teacher/', include(teacher_urls)),
]
