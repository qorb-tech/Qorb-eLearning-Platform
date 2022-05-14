from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Local Import geos here!
from qorb.accounts.models import Student,Teacher

def course_directory_path(inst, file_name):
    return f'course_images/{inst.name}/{file_name}'

def subject_directory_path(inst, file_name):
    return f'course_matrial/{inst.course}/{inst.description}/{file_name}'

def report_directory_path(inst, file_name):
    return f'course_report/{inst.course}/{inst.description_report}/{file_name}'

def students_report_directory_path(inst, file_name):
    return f'student_report/{inst.student}/{inst.report}/{file_name}'

class Course(models.Model):
    student = models.ManyToManyField(Student, null=True, blank=True, related_name='student')
    name = models.CharField(max_length=60, null=True, blank=True, unique=True)
    description = models.TextField(max_length= 200, null=True, blank=True, default='')
    image = models.ImageField(default='course_images/default.png' ,upload_to=course_directory_path, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    
    def __str__(self):
        return str(self.name)    
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'name':self.name})
    
    def get_add_student_url(self):
        return reverse('add_student', kwargs={'name':self.name})

    def get_add_matrial_url(self):
        return reverse('add_matrial', kwargs={'name':self.name})
    
    def get_add_report_url(self):
        return reverse('add_report', kwargs={'name':self.name})

    def create_meeting_url(self):
        return reverse('join_meeting', kwargs={'name': self.name})


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['student', 'course']]
    
    def __str__(self):
        return str(self.student)  

class Subject(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete = models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    description = models.CharField(max_length=400,null=True, blank=True, default='')
    document = models.FileField(upload_to=subject_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("subjects:subject_detail", kwargs={"slug": self.slug})

    def get_courses_related_to_memberships(self):
        return self.courses.all()



#reports model
class Report(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete = models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    description_report = models.CharField(max_length=400,null=True, blank=True, default='')
    document = models.FileField(upload_to=report_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student, through='Report_student')
    deadline = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description_report

    def get_absolute_url(self):
        return reverse("reports:report_detail", kwargs={"slug": self.slug})

    def get_courses_related_to_memberships(self):
        return self.courses.all()

        

class Report_student(models.Model):
    CHOICES = (
        ('لم يتم التسليم','لم يتم التسليم'),
        ('لم يتم التقييم','لم يتم التقييم'),
        ('مقبول','مقبول'),
        ('جيد','جيد'),
        ('جيد جدا','جيد جدا'),
        ('ممتاز','ممتاز'),
        
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to=students_report_directory_path, blank=True, null=True)
    grade = models.CharField(max_length=200,choices=CHOICES,default='لم يتم التسليم')
    teacher_notes=models.TextField( blank=True, null=True)
    student_notes=models.TextField( blank=True, null=True)
    done = models.BooleanField(default=False)
    last_modified = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [['student', 'report']]
    
    def __str__(self):
        return str(self.student) + " : "+ str(self.report)




