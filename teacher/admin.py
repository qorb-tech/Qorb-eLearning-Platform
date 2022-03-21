from django.contrib import admin

# Local imports goes here!
from teacher.models import(
    Course, 
    Subject,
    Report,
    Report_student
)


admin.site.register(Subject)
admin.site.register(Report)
admin.site.register(Report_student)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    prepopulated_fields = {'slug':('name',)}






