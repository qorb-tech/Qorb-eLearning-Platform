from django.urls import path

# local imports goes here
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login_view"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),
]
