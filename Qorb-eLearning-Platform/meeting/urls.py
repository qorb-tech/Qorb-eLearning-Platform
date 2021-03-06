from django.urls import path
from . import views

urlpatterns = [
    path('teacher/courses/join_meeting/<str:name>', views.lobby),
    path('room/', views.room),
    path('get_token/', views.getToken),

    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),

    # SOME_ADDITIONS
    path('student/dashboard/join_meeting/<str:name>', views.lobby),
]