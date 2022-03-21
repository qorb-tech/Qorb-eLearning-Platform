from django.contrib import admin

# Loca imports goes here 
from .models import (
    Quiz,
    QuestionAnswer, 
    QuizStudent
)

class QuestionAnswerInline(admin.TabularInline):
    model = QuestionAnswer

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionAnswerInline]


@admin.register(QuestionAnswer)
class QuestionAnswerAdminAdmin(admin.ModelAdmin):
    list_display = ('question', 'id')
    
admin.site.register(QuizStudent)