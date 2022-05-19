from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
import os 

# local imports goes here
from accounts.models import Teacher

from .models import Course, Report, Report_student, Subject

User = get_user_model()
# <-------------------------- Teacher Profile Form ------------------------------------------>


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "input-i"}),
    )
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"class": "input-i"})
    )

    class Meta:
        model = User
        fields = ["username", "email"]


class UpdateTeacherProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "hidden": "hidden",
                "name": "posti",
                "accept": "image/*",
                "id": "id_posti",
                "class": "img-i-1",
                "onchange": "loadFile(event)",
            }
        )
    )
    age = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "input-i"}),
    )
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "input-i"}),
    )

    class Meta:
        model = Teacher
        fields = ["avatar", "age", "full_name"]


class FormPasswordChange(PasswordChangeForm):

    old_password = forms.CharField(
        label="كلمة المرور القديمة",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password1 = forms.CharField(
        label="كلمة المرور الجديدة",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="تأكيد كلمة المرور الجديدة",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


# <---------------------------------- Teacher Course form -------------------------------------------->


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "name",
            "description",
            "image",
        ]

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "اسم الكورس", "id": "course_name_id"}
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"row": 5, "id": "description_id"})
    )
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "hidden": "hidden",
                "name": "posti",
                "accept": "image/*",
                "id": "id_posti",
                "class": "img-i-1",
                "onchange": "loadFile(event)",
            }
        )
    )


class AddMatrialForm(forms.ModelForm):
    ALLOWED_TYPES = ['pdf']
    document = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "hidden": "hidden",
                "name": "posti",
                "id": "id_posti",
                "class": "img-i-1",
                "onchange": "loadFile()",
            }
        )
    )

    class Meta:
        model = Subject
        fields = (
            "description",
            "document",
        )
    
    def clean(self):
        document = self.cleaned_data.get('document', None)
        if not document:
            raise forms.ValidationError('Missing document file')
        try:
            extension = os.path.splitext(document.name)[1][1:].lower()
            if extension in self.ALLOWED_TYPES:
                return document
            else:
                raise forms.ValidationError('File types is not allowed')
        except Exception as e:
            raise forms.ValidationError('Can not identify file type')


class AddReportForm(forms.ModelForm):
    ALLOWED_TYPES = ['pdf']
    document = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "hidden": "hidden",
                "name": "posti2",
                "id": "id_posti2",
                "class": "img-i-1",
                "onchange": "loadFile2()",
            }
        )
    )

    class Meta:
        model = Report
        fields = (
            "description_report",
            "document",
        )
    
    
    def clean(self):
        document = self.cleaned_data.get('document', None)
        if not document:
            raise forms.ValidationError('Missing document file')
        try:
            extension = os.path.splitext(document.name)[1][1:].lower()
            if extension in self.ALLOWED_TYPES:
                return document
            else:
                raise forms.ValidationError('File types is not allowed')
        except Exception as e:
            raise forms.ValidationError('Can not identify file type')


class UpdateReportGradeForm(forms.ModelForm):
    class Meta:
        model = Report_student
        fields = ["teacher_notes", "grade", "deadline"]

    deadline = forms.DateField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.widgets.DateInput(
            attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
        ),
    )


class UpdateReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["deadline"]

    deadline = forms.DateField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.widgets.DateInput(
            attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
        ),
    )
