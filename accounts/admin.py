from django.contrib import admin

from .models import Contact, Profile, Student, Teacher, User

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Contact)
