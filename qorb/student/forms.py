from attr import field 
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm


# Local imports goes here 
from qorb.accounts.models import Profile, Student
from qorb.teacher.models import Report_student

User = get_user_model()

class UpdateUserForm(forms.ModelForm):
	username = forms.CharField(max_length=100, required=True,
	                           widget=forms.TextInput(attrs={'class': 'input-i'}))
	email = forms.EmailField(required=True, widget=forms.TextInput(
	    attrs={'class': 'input-i'}))

	class Meta:
		model = User
		fields = ['username', 'email']
        


class UpdateStudentProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={
        "hidden":"hidden","name":"posti" ,"accept":"image/*","id":"id_posti",'class':'img-i-1',"onchange":"loadFile(event)" 
    }))
    age = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'input-i'}))
    full_name = forms.CharField(max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'input-i'}))

    
    class Meta:
        model = Student 
        fields = ['avatar', 'age', 'full_name']

    


class FormPasswordChange(PasswordChangeForm):
    
    old_password = forms.CharField(label='كلمة المرور القديمة',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='كلمة المرور الجديدة',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='تأكيد كلمة المرور الجديدة',widget=forms.PasswordInput(attrs={'class': 'form-control'})) 



class UpdateReportForm(forms.ModelForm):
	class Meta:
		model = Report_student
		fields = ['student_notes','report_file']


