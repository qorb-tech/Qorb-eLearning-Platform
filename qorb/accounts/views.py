import json
import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

# local imports goes here
from .decorators import allow_user, unAuth_user
from .forms import ContactForm, LoginForm, SignUpForm


def index(request):
    msg = "None"
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid:
            form.save()
            msg = "Your message sent successfully"
        else:
            msg = "Form is not valid!"
    form = ContactForm()
    context = {"form": form, "msg": msg}

    return render(request, "accounts/index.html", context)


@unAuth_user
def register(request):
    role = None
    msg = None
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            recaptcha_response = request.POST.get("g-recaptcha-response")
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {
                "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                "response": recaptcha_response,
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            # if result['success']:
            if True or result["success"]:
                user = form.save(commit=False)
                if request.POST["role"] == "student":
                    user.is_student = True
                elif request.POST["role"] == "teacher":
                    user.is_teacher = True
                else:
                    user.is_admin = True

                user.save()
                msg = "user created successfully"
                return redirect("login_view")
            else:
                msg = "Invalid reCAPTCHA. Please try again."
        else:
            msg = "form is not valid"
    else:
        form = SignUpForm()

    return render(
        request, "accounts/register.html", {"form": form, "msg": msg, "role": role}
    )


@unAuth_user
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            # recaptcha_response = request.POST.get("g-recaptcha-response")
            # url = "https://www.google.com/recaptcha/api/siteverify"
            # values = {
            #     "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            #     "response": recaptcha_response,
            # }
            # data = urllib.parse.urlencode(values).encode()
            # req = urllib.request.Request(url, data=data)
            # response = urllib.request.urlopen(req)
            # result = json.loads(response.read().decode())
            # if result['success']:

            if True:
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None and user.is_admin:
                    msg = "تم تسجيل الدخول"
                    login(request, user)
                    return redirect("adminpage")
                elif user is not None and user.is_student:
                    msg = "تم تسجيل الدخول"
                    login(request, user)
                    return redirect("student_dashboard")
                elif user is not None and user.is_teacher:
                    msg = "تم تسجيل الدخول"
                    login(request, user)
                    return redirect("teacher_dashboard")
                else:
                    msg = "خطأ فى اسم المستخدم او كلمة المرور"
            else:
                msg = "Invalid reCAPTCHA. Please try again."
        else:
            msg = "يرجى ادخال اسم المستخدم وكلمة المرور"
    else:
        msg = "يرجى ادخال اسم المستخدم وكلمة المرور"
    return render(request, "accounts/login.html", {"form": form, "msg": msg})


@allow_user(["is_teacher", "is_student"])
def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")
