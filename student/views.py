from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
import datetime
from datetime import timezone
import random


# Local imports goes here
from .forms import UpdateUserForm, UpdateStudentProfileForm, FormPasswordChange
from accounts.models import Student, Profile 
from student.forms import UpdateReportForm
from quiz.models import QuizStudent, Quiz, QuestionAnswer
from teacher.models import (Course, Subject, Report,Report_student)




User = get_user_model()

@login_required(login_url='login_view')
def student_dashboard(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'student/student_dashboard.html', context)


@login_required(login_url='login_view')
def profile_student_view(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {'user_profile': user_profile}
    return render(request, 'student/profile_student_view.html', context)


@login_required(login_url='login_view')
def update_student_profile(request):
    msg = None 
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateStudentProfileForm(request.POST, request.FILES, instance=request.user.profile.student)
        if user_form.is_valid() and profile_form.is_valid() :
            user_form.save()
            profile_form.save()
            msg = 'Your profile is updated successfully!'
            return redirect(to='student_dashboard')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateStudentProfileForm(instance=request.user.profile.student)
        

    context = {'user_form': user_form, 'profile_form': profile_form,'user_profile':user_profile, 'msg':msg}
    return render(request, 'student/profile.html', context)

@login_required(login_url='login_view')
def reset_password_view(request):
    user_profile = Profile.objects.get(user=request.user)
    form = FormPasswordChange(request.user)
    if request.method == "POST":
        form = FormPasswordChange(request.user,request.POST)
        if form.is_valid():
            user_form = form.save()
            update_session_auth_hash(request,user_form)
            return redirect('profile_student_view')
            
    context={'form':form,'user_profile': user_profile}
    return render(request, 'student/reset_password.html', context)


@login_required
def courses(request):
    user_profile = Profile.objects.get(user=request.user)
    student = Student.objects.get(user=request.user)
    courses = Course.objects.filter(student=student)
    context = {
        'courses': courses, 
        'user_profile':user_profile
    }
    return render(request, 'student/courses.html', context)



@login_required(login_url='login_view')
def course_detail(request, name):    
    msg=""
    user_profile = Profile.objects.get(user=request.user)
    course = Course.objects.get(name=name)
    student_enrolled = course.student.all()
    teacher = course.teacher
    matrials = Subject.objects.filter(teacher=teacher, course=course).all()
    reports = Report.objects.filter(teacher=teacher, course=course).all()
    grades = Report_student.objects.filter(course__name=course,student__user=request.user)
    context = {
        'course': course, 
        'matrials': matrials,
        'reports': reports, 
        'student_enrolled': student_enrolled,
        "msg":msg, 'user_profile':user_profile,
        'grades':grades
        
    }
    students_list = student_enrolled[::1]
    return render(request, 'student/course_detail.html', context)

@login_required(login_url='login_view')
def upload_report_file(request, id):
    report_grades = Report_student.objects.get(id=id)
    course_name=str(report_grades.course)
    is_deadline_not_over = report_grades.deadline > datetime.datetime.now(timezone.utc)- datetime.timedelta(hours=0)
    if report_grades.deadline > datetime.datetime.now(timezone.utc)- datetime.timedelta(hours=0):

        if request.method == 'POST':
            form = UpdateReportForm(request.POST, request.FILES, instance=report_grades)
            form2 = form.save(commit=False)
            if form.is_valid():
                form2.grade = 'لم يتم التقييم'
                form2.save()
                return redirect('/student/course-detail/'+course_name)

        else:
            form = UpdateReportForm(instance=report_grades)

        return render(request,
                'student/upload-report.html',
                {'form': form,
                'report_grades':report_grades,
                'is_deadline_not_over':is_deadline_not_over})
    else:
        return render(request,
                'student/upload-report.html',
                {'report_grades':report_grades,
                'is_deadline_not_over':is_deadline_not_over})




@login_required(login_url='login_view')
def current_quizzes(request):
    student = Student.objects.get(user=request.user)
    quizzes = QuizStudent.objects.filter(student=student)

    context = {
        'quizzes': quizzes,
        'student':student
    }

    return render(request, 'student/current_quizzes.html', context)


# not completed yet!
@login_required(login_url='login_view')
def start_quiz(request, pk):
    quiz = QuizStudent.objects.get(pk=pk)

    quiz_name = Quiz.objects.filter(name=quiz.quiz.name)[0]

    questions_num = quiz.quiz.number_of_questions
    
    questions = QuestionAnswer.objects.filter(quiz=quiz_name)
    

    questions = list(questions)
    random.shuffle(questions)
    questions = questions[:questions_num]
        
    context = {
        'quiz':quiz,
        'questions':questions,
    }

    if request.method == 'POST':
        data = request.POST
        data = dict(data.lists())
        data.pop('csrfmiddlewaretoken')

        # total_marks = 0 
        # cnt = len(questions)
        # print('questions', questions)

        # i = 1 
        # for q in questions:
        #     # print('correct', q.correct)
        #     # print('q? ', q)
        #     user_answer = request.POST.get(f'answer{i}')
        #     i = i + 1
        #     correct_answer = q.correct
        #     if user_answer == correct_answer:
        #         total_marks += 1

        # print(f'you score {total_marks} out of {cnt}')
        return redirect('current_quizzes')



        
    return render(request, 'student/start_quiz.html', context)

