from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/update/', views.student_update, name='student_update'),
    
    # Enrollment URLs
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/create/', views.enrollment_create, name='enrollment_create'),
    
    # Assignment URLs
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    
    # Exam URLs
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/<int:pk>/', views.exam_detail, name='exam_detail'),
]
