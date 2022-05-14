from django.urls import path
from . import views

urlpatterns = [
    path('adminpage/', views.admin, name='adminpage'),
]
