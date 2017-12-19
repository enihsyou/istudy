# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.urls import path, include

from web import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.logout, name='logout'),
    path('course/', include([
        path('list/', views.CourseListView.as_view(), name='course_list'),
        path('new/', views.CourseCreateView.as_view(), name='course_create'),
        path('<int:pk>/', views.LessonListView.as_view(), name='lesson_list'),
        path('<int:course>/<int:lesson>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    ])),
    path('paper/', include([
        path('list/', views.PaperListView.as_view(), name='paper_list'),
        path('<int:pk>/', views.PaperDetailView.as_view(), name='paper_detail'),
    ])),
    path('student/', include([
        path('signup/', views.StudentCreateView.as_view(), name='student_create'),
        path('login/', views.StudentLoginView.as_view(), name='student_login'),
        path('<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
        path('<int:pk>/edit', views.StudentUpdateView.as_view(), name='student_edit'),
        path('<int:pk>/delete', views.StudentDeleteView.as_view(), name='student_delete'),
        path('course/', include([
            path('list/', views.StudentCourseListView.as_view(), name='student_course_list'),
            path('<int:pk>/join/', views.course_join_view, name='student_join_course')
        ]))
    ])),
    path('teacher/', include([
        path('signup/', views.TeacherCreateView.as_view(), name='teacher_create'),
        path('login/', views.TeacherLoginView.as_view(), name='teacher_login'),
        path('<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
        path('<int:pk>/edit', views.TeacherUpdateView.as_view(), name='teacher_edit'),
        path('<int:pk>/delete', views.TeacherDeleteView.as_view(), name='teacher_delete'),
        path('<int:pk>/course/', include([
            path('list/', views.TeacherCourseListView.as_view(), name='teacher_course_list'),
            path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
            path('<int:pk>/edit', views.CourseUpdateView.as_view(), name='course_edit'),
            path('<int:pk>/delete', views.CourseDeleteView.as_view(), name='course_delete'),
        ]))
    ])),
]
