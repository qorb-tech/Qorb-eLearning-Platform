from django.shortcuts import render


def admin(request):
    return render(request, "adminDashboard/admin.html")
