from django.contrib import admin

# Local imports goes here!
from qorb.teacher.models import Course, Report, Report_student, Subject

admin.site.register(Subject)
admin.site.register(Report)
admin.site.register(Report_student)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher")
    prepopulated_fields = {"slug": ("name",)}
