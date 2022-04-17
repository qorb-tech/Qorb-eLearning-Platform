from django.shortcuts import redirect
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model

# Local imports goes here!
from teacher.models import Course
from accounts.models import Student 
from quiz.models import QuizStudent, Quiz


User = get_user_model()

def unAuth_user(view_fun):
    def wrapper_fun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_fun(request, *args, **kwargs)
    return wrapper_fun


def allow_user(user_permission_list):
    def decorator(view_func):
        def inner(request, *args, **kwargs):
            user = []
            if request.user.is_teacher:
                user.append("is_teacher")
            elif request.user.is_student:
                user.append("is_student")

            if user[0] not in user_permission_list:
                raise Http404()
            else:
                return view_func(request, *args, **kwargs)
        return inner
    return decorator


def allow_courses_student():
    def decorator(view_func):
        def inner(request, *args, **kwargs):
            course = get_object_or_404(Course, name=kwargs.get('name'))
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
                quiz = get_object_or_404(QuizStudent, pk=kwargs.get('pk'))
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