from django.contrib import admin

# Loca imports goes here
from .models import QuestionAnswer, Quiz, QuizStudent


class QuestionAnswerInline(admin.TabularInline):
    model = QuestionAnswer


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionAnswerInline]


@admin.register(QuestionAnswer)
class QuestionAnswerAdminAdmin(admin.ModelAdmin):
    list_display = ("question", "id")


@admin.register(QuizStudent)
class QuizStudentAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz")
