from django import forms

# Local imports goes here!
from .models import Quiz, QuestionAnswer
from qorb.accounts.models import Profile, Teacher
from qorb.teacher.models import  Course
from config.current_user import get_current_user



class CreateQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('id', 'course', 'name', 'number_of_questions', 'time')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        teacher = Teacher.objects.get(user=get_current_user())
        course = Course.objects.filter(teacher=teacher)
        self.fields['course'].queryset  = course
  
  
class CreateQuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = ('id', 'question', 'option1','option2', 'option3', 'option4', 'correct')



