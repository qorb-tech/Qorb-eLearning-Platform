from django.urls import include, path

# Local Imports Goes Here!
from .views import (
    add_course,
    course_detail,
    courses,
    delete_course,
    delete_report,
    delete_student,
    delete_subject,
    edit_course,
    edit_report_deadline,
    lecs_page_select,
    profile_techear_view,
    report_grades_records_view,
    report_grades_update,
    reports_page_select,
    reset_password_view,
    students_page_select,
    teacher_dashboard,
    update_teacher_profile,
    schedule_meeting,
    join_course_list,
    confirm_join_course,
    confirm_delete_request, 
    show_graph,
)

urlpatterns = [
    # teacher profile routes
    path("dashboard/", teacher_dashboard, name="teacher_dashboard"),

    path("join-course/", join_course_list, name="join_course_list"),
    path("join-course/confirm/<str:name>/<str:std_name>/", confirm_join_course, name="confirm_join_course"),
    path("join-course/dismiss/<str:name>/<str:std_name>/", confirm_delete_request, name="confirm_delete_request"),


    path("update-profile", update_teacher_profile, name="update_teacher_profile"),
    path("profile-info", profile_techear_view, name="profile_techear_view"),
    path("reset-password", reset_password_view, name="reset_password_view"),
    # courses routes
    path("courses/", courses, name="courses"),
    path("add-course/", add_course, name="add_course"),
    path("edit-course/<str:name>/", edit_course, name="edit_course"),
    path("delete-course/<str:name>/", delete_course, name="delete_course"),
    path("course-detail/<str:name>/", course_detail, name="course_detail"),
    path("delete-subject/<int:pk>/", delete_subject, name="delete_subject"),
    path("delete-report/<int:pk>/", delete_report, name="delete_report"),
    path("delete-student/<str:name>/<int:pk>/", delete_student, name="delete_student"),
    # select page
    path("lecs-page-select/", lecs_page_select, name="lecs_page_select"),
    path("reports-page-select/", reports_page_select, name="reports_page_select"),
    path("students-page-select/", students_page_select, name="students_page_select"),
    # grades
    path(
        "report_grades/<int:id>/change/",
        report_grades_update,
        name="report-grades-detail",
    ),
    path(
        "report-grades-view/<str:course>/<str:report>/",
        report_grades_records_view,
        name="report-grades-view",
    ),
    path(
        "edit-report-deadline/<int:pk>/",
        edit_report_deadline,
        name="edit-report-deadline",
    ),
    path('schedule_meeting/<str:name>', schedule_meeting, name='schedule-meeting'),
    path("show-graph/<str:name>/", show_graph, name="show_graph"),


]
