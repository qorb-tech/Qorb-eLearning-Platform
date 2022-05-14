from django.contrib import admin
from .models import User , Contact,Profile, Student, Teacher

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Contact)