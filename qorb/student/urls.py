from django.urls import path
from . import views
from .views import course_detail,upload_report_file

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile-info', views.profile_student_view,name='profile_student_view'),
    path('update-profile', views.update_student_profile, name='update_student_profile'),
    path('reset-password', views.reset_password_view,name='reset_password_view'),
    path('courses/', views.courses, name='student_courses'),

    path('course-detail/<str:name>/', course_detail, name='course_detail'),
    path('upload-report-file/<int:id>/', upload_report_file, name='upload_report_file'),



    
    path('current-quizzes', views.current_quizzes, name='current_quizzes'),
    path('start-quiz/<int:pk>/', views.start_quiz, name='start_quiz'),


]





