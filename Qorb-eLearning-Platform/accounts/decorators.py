from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from accounts.models import Student
from quiz.models import Quiz, QuizStudent
# Local imports goes here!
from teacher.models import Course

User = get_user_model()


def unAuth_user(view_fun):
    def wrapper_fun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return view_fun(request, *args, **kwargs)

    return wrapper_fun

#########################################################
def allow_user(user_permission_list):
    def decorator(view_func):
        def inner(request, *args, **kwargs):
            try:
                if request.user.is_teacher:
                    return view_func(request, *args, **kwargs)
                elif request.user.is_student:
                    return view_func(request, *args, **kwargs)
                elif request.user.is_admin:
                    return view_func(request, *args, **kwargs)
                else:
                    logout(request)
                    return redirect("/")
            except:
                logout(request)
                return redirect("/")
        return inner
    return decorator

#########################################################

def allow_courses_student():
    def decorator(view_func):
        def inner(request, *args, **kwargs):
            course = get_object_or_404(Course, name=kwargs.get("name"))
            student = Student.objects.get(user=request.user)
            res = Course.objects.filter(student=student)

            if course in res:
                return view_func(request, *args, **kwargs)
            else:
                raise Http404()

        return inner

    return decorator


def allow_quiz_student():
    def decorator(view_func):
        def inner(request, *args, **kwargs):
            try:
                quiz = get_object_or_404(QuizStudent, pk=kwargs.get("pk"))
                # user quizzes
                student = Student.objects.get(user=request.user)
                quizzes = QuizStudent.objects.filter(student=student)

            except quiz.DoesNotExist:
                return HttpResponse("No Quizzes yet!")
            if quiz in quizzes:
                return view_func(request, *args, **kwargs)
            else:
                raise Http404()

        return inner

    return decorator
