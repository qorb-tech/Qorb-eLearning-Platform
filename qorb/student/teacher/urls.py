from django.urls import path

# Local Imports Goes Here!
from .views import (
    courses , course_detail, 
    profile_techear_view,
    teacher_dashboard,
    update_teacher_profile,
    add_course, delete_subject,
    delete_report,
    delete_student,
    lecs_page_select,
    students_page_select,
    reports_page_select,
    reset_password_view,
    report_grades_update,
    report_grades_records_view,
    edit_course,
    delete_course,
    edit_report_deadline
    )

urlpatterns = [
    # teacher profile routes
    path('dashboard/',teacher_dashboard, name='teacher_dashboard'),
    path('update-profile', update_teacher_profile,name='update_teacher_profile'),
    path('profile-info', profile_techear_view,name='profile_techear_view'),
    path('reset-password', reset_password_view,name='reset_password_view'),
    
    # courses routes
    path('courses/', courses, name='courses'),
    path('add-course/', add_course, name='add_course'),
    path('edit-course/<str:name>/', edit_course, name='edit_course'),
    path('delete-course/<str:name>/', delete_course, name='delete_course'),
    path('course-detail/<str:name>/', course_detail, name='course_detail'),
    path('delete-subject/<int:pk>/', delete_subject, name='delete_subject'),
    path('delete-report/<int:pk>/', delete_report, name='delete_report'),
    path('delete-student/<str:name>/<int:pk>/', delete_student, name='delete_student'),

    #select page
    path('lecs-page-select/', lecs_page_select, name='lecs_page_select'),
    path('reports-page-select/', reports_page_select, name='reports_page_select'),
    path('students-page-select/', students_page_select, name='students_page_select'),

    #grades
    path('report_grades/<int:id>/change/', report_grades_update, name='report-grades-detail'),
    path('report-grades-view/<str:course>/<str:report>/', report_grades_records_view, name='report-grades-view'),
    path('edit-report-deadline/<int:pk>/', edit_report_deadline, name='edit-report-deadline'),

     
]


