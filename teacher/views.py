import datetime
import re

from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from datetime import timezone


# Local imports goes here
from accounts.decorators import allow_user
from accounts.models import Profile, Student, Teacher

from .forms import (
    AddCourseForm,
    AddMatrialForm,
    AddReportForm,
    FormPasswordChange,
    UpdateReportForm,
    UpdateReportGradeForm,
    UpdateTeacherProfileForm,
    UpdateUserForm,
    schedule_meeting_form,
)
from .models import Course, Report, Report_student, Subject, meetings, JoinCourseList

User = get_user_model()


@login_required(login_url="login_view")
@allow_user(["is_teacher"])
def teacher_dashboard(request):
    user_profile = Profile.objects.get(user=request.user)
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(teacher=teacher)
    try:
        dic = {}
        all_rooms = meetings.objects.all()
        for c in courses:
            for r in all_rooms:
                if str(c)==str(r) :
                    is_deadline_not_over = r.meeting_date > datetime.datetime.now(timezone.utc) - datetime.timedelta(hours=0)
                    if is_deadline_not_over:
                        dic[c]=r.meeting_date
        context = {"courses": courses, "user_profile": user_profile,"dic":dic}
    except:
        context = {"courses": courses, "user_profile": user_profile}
    
    return render(request, "teacher/teacher_dashboard.html", context)


@login_required(login_url="login_view")
@allow_user(["is_teacher"])
def update_teacher_profile(request):
    msg = None
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateTeacherProfileForm(
            request.POST, request.FILES, instance=request.user.profile.teacher
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            msg = "Your profile is updated successfully!"
            return redirect(to="teacher_dashboard")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateTeacherProfileForm(instance=request.user.profile.teacher)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "user_profile": user_profile,
        "msg": msg,
    }
    return render(request, "teacher/profile.html", context)


# change password view
@login_required(login_url="login_view")
@allow_user(["is_teacher"])
def reset_password_view(request):
    user_profile = Profile.objects.get(user=request.user)
    form = FormPasswordChange(request.user)
    if request.method == "POST":
        form = FormPasswordChange(request.user, request.POST)
        if form.is_valid():
            user_form = form.save()
            update_session_auth_hash(request, user_form)

    context = {"form": form, "user_profile": user_profile}
    return render(request, "teacher/reset_password.html", context)


# Profile View
@login_required(login_url="login_view")
@allow_user(["is_teacher"])
def profile_techear_view(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {"user_profile": user_profile}
    return render(request, "teacher/profile_teach_view.html", context)


# <----------------------- Courses views ------------------------------->


@login_required
@allow_user(["is_teacher"])
def courses(request):
    user_profile = Profile.objects.get(user=request.user)
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(teacher=teacher)
    context = {"courses": courses, "user_profile": user_profile}
    return render(request, "teacher/courses.html", context)


@login_required
@allow_user(["is_teacher"])
def edit_course(request, name):
    course = Course.objects.get(name=name)
    if request.method == "POST":
        form = AddCourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect("courses")

    else:
        form = AddCourseForm(instance=course)
    context = {"form": form}
    return render(request, "teacher/edit_course.html", context)


@login_required
@allow_user(["is_teacher"])
def delete_course(request, name):
    course = Course.objects.get(name=name)
    course.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url='login_view')
@allow_user(['is_teacher'])
def course_detail(request, name):
    # Add Lecture  View
    msg=""
    user_profile = Profile.objects.get(user=request.user)
    course = Course.objects.get(name=name)
    student_enrolled = course.student.all()
    teacher = Teacher.objects.get(user=request.user)

    if course.teacher != teacher:
        raise Http404

    matrials = Subject.objects.filter(teacher=teacher, course=course).all()
    reports = Report.objects.filter(teacher=teacher, course=course).all()
    if request.method == 'POST':
        add_lec_form = AddMatrialForm(request.POST, request.FILES)
        if add_lec_form.is_valid() and (bool(str(request.POST.get('description')).strip()) and str(request.POST.get('description'))!="None"):
            temp = add_lec_form.save(commit=False)
            teacher = Teacher.objects.get(user=request.user)
            course = Course.objects.get(name=name)
            temp.teacher = teacher
            temp.course = course
            temp.save()
            msg = "تم اضافه المحاضره"
            request.session['vote']="lecs-page"

    else:
        add_lec_form = AddMatrialForm()

    # Add Student to Course View
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    course = Course.objects.get(name=name)

    if q is not '':
        try:
            student = Student.objects.get(email=q)
            course = Course.objects.get(name=name)
            course.student.add(student)
            msg = "تم اضافه الطالب للكورس"
            request.session['vote']="student-page"
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        except:
            request.session['vote']="student-page"
            msg = "الايميل غير موجود"
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    # Add Report View
    if  request.method == 'POST':
        add_report_form = AddReportForm(request.POST, request.FILES)

        if add_report_form.is_valid() and (bool(str(request.POST.get('description_report')).strip()) and str(request.POST.get('description_report'))!="None")  :
            temp = add_report_form.save(commit=False)
            teacher = Teacher.objects.get(user=request.user)
            course = Course.objects.get(name=name)
            temp.teacher = teacher
            temp.course = course
            temp.save()

            try:
                students = Course.objects.filter(name=course).values('student')
                if(students[0]['student']!= None):
                    temp.save()
                else:
                    msg = "لا يوجد طلاب فى الكورس برجاء اضافه طلاب اولا"
                for i in students:
                    student_name = Student.objects.get(id=i['student'])
                    report_name = Report.objects.get(description_report = temp.description_report)
                    student_in_quiz = Report_student(student=student_name, course=course, report=report_name, grade='لم يتم التسليم')
                    student_in_quiz.save()
            except:
                msg = "ERROR"
            msg = "تم اضافه التقرير"
            request.session['vote']="reports-page"

    else:
        add_report_form = AddReportForm()
    context = {
        'course': course,
        'matrials': matrials,
        'reports': reports,
        'add_lec_form': add_lec_form,
        'student_enrolled': student_enrolled,
        "msg":msg, 'user_profile':user_profile,
        'msg': msg, 'add_report_form': add_report_form,


    }
    return render(request, 'teacher/course_detail.html', context)


@login_required(login_url='login_view')
@allow_user(['is_teacher'])
def add_course(request):
    msg = None
    if request.method == 'POST':
        course_form = AddCourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            teacher = Teacher.objects.get(user=request.user)
            course.teacher = teacher
            course.save()
            messages.success(request, 'Your course is created successfully!')
            return redirect('courses')
        else:
            msg = 'error validating form'
            return HttpResponse('course name already exists choose another name!')
    else:
        course_form = AddCourseForm(instance=request.user.profile.teacher)
    context = {'course_form': course_form, 'msg': msg}
    return render(request, 'teacher/add_course.html', context)



@login_required(login_url="login_view")
@allow_user(["is_teacher"])
def add_course(request):
    msg = None
    if request.method == "POST":
        course_form = AddCourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            teacher = Teacher.objects.get(user=request.user)
            course.teacher = teacher
            course.save()
            messages.success(request, "Your course is created successfully!")
            return redirect("courses")
        else:
            msg = "error validating form"
            return HttpResponse("course name already exists choose another name!")
    else:
        course_form = AddCourseForm(instance=request.user.profile.teacher)
    context = {"course_form": course_form, "msg": msg}
    return render(request, "teacher/add_course.html", context)


@login_required(login_url="login_view")
@allow_user(["is_teacher"])
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, id=pk)
    subject.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="login_view")
@allow_user(["is_teacher"])
def delete_report(request, pk):
    report = get_object_or_404(Report, id=pk)
    report.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="login_view")
@allow_user(["is_teacher"])
def delete_student(request, name, pk):
    student = Student.objects.get(id=pk)
    course = Course.objects.get(name=name)
    course.student.remove(student)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


# PAGE SELECT
@login_required(login_url="login_view")
@allow_user(["is_teacher", "is_student"])
def lecs_page_select(request):
    request.session["vote"] = "lecs-page"
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="login_view")
@allow_user(["is_teacher", "is_student"])
def reports_page_select(request):
    request.session["vote"] = "reports-page"
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url="login_view")
@allow_user(["is_teacher", "is_student"])
def students_page_select(request):
    request.session["vote"] = "student-page"
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


# update grades for reports

@login_required(login_url='login_view')
@allow_user(['is_teacher'])
def report_grades_update(request, id):
    report_grades = Report_student.objects.get(id=id)
    course_name=str(report_grades.course)
    report_name = str(report_grades.report)
    
    teacher = Teacher.objects.get(user=request.user)
    
    #check if teacher is the course owener or not
    if report_grades.course.teacher != teacher:
        raise Http404

    if request.method == 'POST':
        form = UpdateReportGradeForm(request.POST, instance=report_grades)
        new_form = form.save(commit=False)
        if form.is_valid():
            if report_grades.grade !='لم يتم التسليم':
                new_form.done = True
            else:
                new_form.done = False
            new_form.save()
            return redirect('report-grades-view',course=course_name,report=report_name)
            
    else:
        form = UpdateReportGradeForm(instance=report_grades)

    return render(request,
                'teacher/report-grades-detail.html',
                {'form': form,
                'report_grades':report_grades})


@login_required(login_url="login_view")
@allow_user(["is_teacher"])
def report_grades_records_view(request, course, report):
    report_grades = Report_student.objects.filter(
        course__name=course, report__description_report=report
    )

    # check if teacher is the course owener or not
    report_owner = Report_student.objects.get(
        course__name=course, report__description_report=report
    )
    teacher = Teacher.objects.get(user=request.user)
    if report_owner.report.teacher != teacher:
        raise Http404

    return render(
        request, "teacher/report-grades-view.html", {"report_grades": report_grades}
    )


@login_required(login_url="login_view")
@allow_user(["is_teacher"])
def edit_report_deadline(request, pk):
    report = Report.objects.get(id=pk)

    # check if teacher is the course owener or not
    teacher = Teacher.objects.get(user=request.user)
    if report.teacher != teacher:
        raise Http404

    if request.method == "POST":
        form = UpdateReportForm(request.POST, instance=report)
        new_form = form.save(commit=False)
        dead_line = datetime.datetime.strptime(
            form["deadline"].value() + ":00.000-0000", "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        new_form.deadline = dead_line
        if form.is_valid():
            new_form.save()
            return redirect(to="teacher_dashboard")
    else:
        form = UpdateReportForm()

    context = {"form": form}
    return render(request, "teacher/edit_report_deadline.html", context)


@login_required(login_url='login_view')
def schedule_meeting(request,name):

    course= Course.objects.get(name=name)
    if course.teacher != Teacher.objects.get(user=request.user):
        raise Http404

    if request.method == 'POST':
        form = schedule_meeting_form(request.POST)
        new_form = form.save(commit=False)
        new_form.teacher=Teacher.objects.get(user=request.user)
        new_form.course=Course.objects.get(name=name)
        meeting_date = datetime.datetime.strptime(form['meeting_date'].value()+":00.000-0000",'%Y-%m-%dT%H:%M:%S.%f%z')
        new_form.meeting_date = meeting_date
        new_form.description_meeting=Course.objects.get(name=name)
        if form.is_valid():
            new_form.save()
            return redirect('teacher_dashboard')
            
    else:
        form = schedule_meeting_form()

    return render(request,
                'teacher/schedule_meeting.html',
                {'form': form})


def join_course_list(request, *args, **kwargs):
    teacher = Teacher.objects.get(user=request.user)
    teacher_courses = Course.objects.filter(teacher=teacher)
    all_requests = JoinCourseList.objects.filter(teacher=teacher)
    context = {"all_requests":all_requests,"teacher_courses":teacher_courses}
    return render(request, "teacher/join_course_list.html", context)

def confirm_join_course(request, *args, **kwargs):
    course = Course.objects.get(name=kwargs['name'])
    temp = User.objects.get(username=kwargs['std_name'])
    student = Student.objects.get(user=temp)
    course.student.add(student)
    messages.success(request, "تم اضافه الطالب بنجاح")
    JoinCourseList.objects.filter(student=student, course=course).delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))    
    
def confirm_delete_request(request, *args, **kwargs):
    course = Course.objects.get(name=kwargs['name'])
    temp = User.objects.get(username=kwargs['std_name'])
    student = Student.objects.get(user=temp)
    JoinCourseList.objects.filter(student=student, course=course).delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))  


def show_graph(request, name):
    course = Course.objects.get(name=name)
    return render(request, "teacher/show_graph.html", {"name":name})


