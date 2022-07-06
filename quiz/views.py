from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

# Local imports goes here!
from accounts.models import Profile, Student
from teacher.models import Course, Teacher

from .forms import CreateQuestionAnswerForm, CreateQuizForm
from .models import QuestionAnswer, Quiz, QuizStudent


@login_required(login_url="login_view")
def quizzes(request):
    auther = Teacher.objects.get(user=request.user)
    quizzes = Quiz.objects.filter(auther=auther)
    user_profile = Profile.objects.get(user=request.user)

    msg = ""
    if request.method == "POST":
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            # course = Course.objects.get(teacher=request.user.id)
            temp = form.save(commit=False)
            auther = Teacher.objects.get(user=request.user)
            temp.auther = auther
            course = temp.course
            # temp.save()
            try:
                students = Course.objects.filter(name=course).values("student")
                if students[0]["student"] != None:
                    temp.save()
                else:
                    msg = "لا يوجد طلاب فى الكورس برجاء اضافه طلاب اولا"
                    return render(
                        request, "quiz/quiz_list.html", {"form": form, "msg": msg}
                    )
                for i in students:
                    student_name = Student.objects.get(id=i["student"])
                    quiz_name = Quiz.objects.get(name=temp.name)
                    student_in_quiz = QuizStudent(
                        student=student_name, course=course, quiz=quiz_name
                    )
                    student_in_quiz.save()
            except:
                msg = "ERROR"
                return render(
                    request, "quiz/quiz_list.html", {"form": form, "msg": msg}
                )
        else:
            msg = "form is not valid"
        return redirect("quizzes")
    else:

        form = CreateQuizForm()
    return render(
        request,
        "quiz/quiz_list.html",
        {"quizzes": quizzes, "user_profile": user_profile, "form": form, "msg": msg},
    )


@login_required(login_url="login_view")
def create_question(request, pk):
    quiz = Quiz.objects.get(id=pk)
    questions = QuestionAnswer.objects.filter(quiz=quiz)
    form = CreateQuestionAnswerForm(request.POST or None)
    msg = None
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        if form.is_valid():
            try:
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()
                return redirect("detail_question", pk=question.id)
            except:
                msg = "Question already exists!"
                return render(
                    request,
                    "quiz/partials/create_question_answer_form.html",
                    context={"form": form, "msg": msg},
                )
        else:
            return render(
                request,
                "quiz/partials/create_question_answer_form.html",
                context={"form": form, "msg": msg},
            )

    context = {
        "form": form,
        "questions": questions,
        "quiz": quiz,
        "user_profile": user_profile,
    }
    return render(request, "quiz/create_question_answer.html", context)


@login_required(login_url="login_view")
def create_question_form(request):
    form = CreateQuestionAnswerForm()
    context = {
        "form": form,
    }
    return render(request, "quiz/partials/create_question_answer_form.html", context)


def delete_question(request, pk):
    question = get_object_or_404(QuestionAnswer, id=pk)
    if request.method == "POST":
        question.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


@login_required(login_url="login_view")
def detail_question(request, pk):
    question = get_object_or_404(QuestionAnswer, id=pk)
    context = {
        "question": question,
    }
    return render(request, "quiz/partials/quiz_detail.html", context)


@login_required(login_url="login_view")
def update_question(request, pk):
    question = get_object_or_404(QuestionAnswer, id=pk)
    form = CreateQuestionAnswerForm(request.POST or None, instance=question)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("detail_question", pk=question.id)
    context = {
        "question": question,
        "form": form,
    }

    return render(request, "quiz/partials/create_question_answer_form.html", context)
