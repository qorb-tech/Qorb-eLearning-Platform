import datetime
import random
from ast import Return
from datetime import timezone

from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

# Local imports goes here
from qorb.accounts.decorators import allow_courses_student, allow_user
from qorb.accounts.models import Profile, Student
from qorb.quiz.models import QuestionAnswer, Quiz, QuizStudent
from qorb.student.forms import UpdateReportForm
from qorb.teacher.models import Course, Report, Report_student, Subject

from .forms import FormPasswordChange, UpdateStudentProfileForm, UpdateUserForm

User = get_user_model()

@login_required(login_url="login_view")
@allow_user(["is_student"])
def student_dashboard(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {"user_profile": user_profile}
    return render(request, "student/student_dashboard.html", context)


@require_http_methods(['POST'])
@login_required(login_url="login_view")
@allow_user(["is_student"])
def search(request):
    search = request.POST['search']
    flag = False
    if search is not None:
        flag = True
    student = Student.objects.get(user=request.user)
    student_courses = Course.objects.filter(student=student)
    courses = Course.objects.filter(name__icontains=search).exclude(
        name__in= student_courses.values_list('name', flat=True)
    )
    return render(request, 'student/search.html', {'courses': courses, 'flag':flag})

@login_required(login_url="login_view")
@allow_user(["is_student"])
def join_course(request, name):
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(name=name)
    course.student.add(student)
    msg = "تم اضافه الطالب للكورس"
    context = {"msg":msg}
    return render(request, "student/student_dashboard.html", context)


@login_required(login_url="login_view")
@allow_user(["is_student"])
def profile_student_view(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {"user_profile": user_profile}
    return render(request, "student/profile_student_view.html", context)


@login_required(login_url="login_view")
@allow_user(["is_student"])
def update_student_profile(request):
    msg = None
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateStudentProfileForm(
            request.POST, request.FILES, instance=request.user.profile.student
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            msg = "Your profile is updated successfully!"
            return redirect(to="student_dashboard")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateStudentProfileForm(instance=request.user.profile.student)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "user_profile": user_profile,
        "msg": msg,
    }
    return render(request, "student/profile.html", context)


@login_required(login_url="login_view")
@allow_user(["is_student"])
def reset_password_view(request):
    user_profile = Profile.objects.get(user=request.user)
    form = FormPasswordChange(request.user)
    if request.method == "POST":
        form = FormPasswordChange(request.user, request.POST)
        if form.is_valid():
            user_form = form.save()
            update_session_auth_hash(request, user_form)
            return redirect("profile_student_view")

    context = {"form": form, "user_profile": user_profile}
    return render(request, "student/reset_password.html", context)


@login_required
@allow_user(["is_student"])
def courses(request):
    user_profile = Profile.objects.get(user=request.user)
    student = Student.objects.get(user=request.user)
    courses = Course.objects.filter(student=student)
    context = {"courses": courses, "user_profile": user_profile}
    return render(request, "student/courses.html", context)


@login_required(login_url="login_view")
@allow_user(["is_student"])
@allow_courses_student()
def course_detail(request, name):
    msg = ""
    user_profile = Profile.objects.get(user=request.user)
    course = Course.objects.get(name=name)
    student_enrolled = course.student.all()

    # students_ids = []
    # for user in student_enrolled.values_list():
    #     students_ids.append(user[0])
    #     print(user[0],)
    # if request.user.id in students_ids:
    #     print("**************")
    # print(request.user.id)

    teacher = course.teacher
    matrials = Subject.objects.filter(teacher=teacher, course=course).all()
    reports = Report.objects.filter(teacher=teacher, course=course).all()
    grades = Report_student.objects.filter(
        course__name=course, student__user=request.user
    )
    context = {
        "course": course,
        "matrials": matrials,
        "reports": reports,
        "student_enrolled": student_enrolled,
        "msg": msg,
        "user_profile": user_profile,
        "grades": grades,
    }
    students_list = student_enrolled[::1]
    return render(request, "student/course_detail.html", context)


@login_required(login_url="login_view")
@allow_user(["is_student"])
def upload_report_file(request, id):
    report_grades = Report_student.objects.get(id=id)

    if str(report_grades.student) != str(request.user):
        raise Http404()

    course_name = str(report_grades.course)
    report = Report.objects.get(description_report=report_grades.report)
    is_deadline_not_over = report.deadline > datetime.datetime.now(
        timezone.utc
    ) - datetime.timedelta(hours=0)
    if report.deadline > datetime.datetime.now(timezone.utc) - datetime.timedelta(
        hours=0
    ):

        if request.method == "POST":
            form = UpdateReportForm(request.POST, request.FILES, instance=report_grades)
            form2 = form.save(commit=False)
            form2.grade = "لم يتم التقييم"
            if form.is_valid():
                form2.save()
                return redirect("/student/course-detail/" + course_name)

        else:
            form = UpdateReportForm(instance=report_grades)

        return render(
            request,
            "student/upload-report.html",
            {
                "form": form,
                "report_grades": report_grades,
                "is_deadline_not_over": is_deadline_not_over,
                "report": report,
            },
        )
    else:
        return render(
            request,
            "student/upload-report.html",
            {
                "report_grades": report_grades,
                "is_deadline_not_over": is_deadline_not_over,
                "report": report,
            },
        )


@login_required(login_url="login_view")
@allow_user(["is_student"])
def current_quizzes(request):
    student = Student.objects.get(user=request.user)
    quizzes = QuizStudent.objects.filter(student=student)

    context = {"quizzes": quizzes, "student": student}

    return render(request, "student/current_quizzes.html", context)


@login_required(login_url="login_view")
@allow_user(["is_student"])
def start_quiz(request, pk):
    quiz = QuizStudent.objects.get(pk=pk)

    # check if student do the exam before
    if quiz.done:
        raise Http404()

    quiz_name = Quiz.objects.filter(name=quiz.quiz.name)[0]
    quiz_time = quiz_name.time
    if str(quiz.student) != str(request.user):
        raise Http404()

    questions_num = quiz.quiz.number_of_questions

    questions = QuestionAnswer.objects.filter(quiz=quiz_name)

    questions = list(questions)
    # random.shuffle(questions)
    questions = questions[:questions_num]

    if request.method == "POST":
        data = request.POST
        data = dict(data.lists())
        data.pop("csrfmiddlewaretoken")

        i = 1
        quiz.score = 0
        for q in questions:
            user_answer = request.POST.get(f"answer{i}")
            correct_answer = q.correct
            i += 1
            if user_answer == correct_answer:
                quiz.score += 1
        quiz.total_marks = len(questions)
        quiz.done = True
        quiz.save()
        return redirect("current_quizzes")

    context = {
        "quiz": quiz,
        "quiz_time": quiz_time,
        "questions": questions,
    }
    return render(request, "student/start_quiz.html", context)
