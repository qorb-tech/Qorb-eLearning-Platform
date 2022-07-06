from django.contrib import admin

# Local imports goes here!
from teacher.models import Course, Report, Report_student, Subject ,meetings

admin.site.register(Subject)
admin.site.register(Report)
admin.site.register(Report_student)
admin.site.register(meetings)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "teacher")
    prepopulated_fields = {"slug": ("name",)}
