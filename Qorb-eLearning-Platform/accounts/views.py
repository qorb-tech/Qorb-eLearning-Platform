import json
import urllib.request

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
    flag = False

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
                    flag = True
                    user.is_student = True

                elif request.POST["role"] == "teacher":
                    flag = True
                    user.is_teacher = True
                else:
                    flag = True
                    user.is_admin = True
                user.save()
                messages.success(request, "Registration successful.")
                request.session['flag'] = True
                #redirect(reverse('login_view', kwargs={ 'flag': flag }))
                return redirect('login_view')
                # return redirect("login_view", kwargs={'flag': flag})
                # return HttpResponseRedirect(reverse('create_rating', args=(flag,)))
                #return render(
                #    request, "accounts/login.html", {"flag": flag}
                #)
            else:
                messages.error(request, "Invalid reCAPTCHA. Please try again.")

        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = SignUpForm()

    return render(
        request, "accounts/register.html", {"form": form, "flag": flag, "role": role}
    )


@unAuth_user
def login_view(request):
    form = LoginForm(request.POST or None)
    flag = False

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
                    flag = True
                    login(request, user)
                    messages.success(request, "Login successfully.")   
                    return redirect("adminpage")

                elif user is not None and user.is_student:
                    flag = True
                    login(request, user)
                    messages.success(request, "Login successfully.")   
                    return redirect("student_dashboard")

                elif user is not None and user.is_teacher:
                    flag = True
                    login(request, user)
                    messages.success(request, "Login successfully.")   
                    return redirect("teacher_dashboard")

                else:
                    messages.error(request, "Unsuccessful login. Invalid information.")

            else:
                messages.error(request, "Invalid reCAPTCHA. Please try again.")

        else:
            messages.error(request, "Unsuccessful login. Invalid information.")
    return render(request, "accounts/login.html", {"form": form, "flag": flag})


@allow_user(["is_teacher", "is_student"])
def logout_user(request):
    logout(request)
    messages.info(request, "You Logged out.")
    return redirect("/")


