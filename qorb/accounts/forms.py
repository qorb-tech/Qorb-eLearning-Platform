from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
# Local imports goes here!
from .models import User
from .models import Contact
User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
           attrs={'placeholder': 'اسم المستخدم',
           'id': 'username'
           }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': ' كلمه المرور',
            'id': 'password1'
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'اسم المستخدم'}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'كلمة المرور',
            'id': 'password1'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'تأكيد كلمة المرور',
            'id': 'password2'
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
             attrs={'placeholder': 'البريد الالكتروني'}
        ),
 #       error_messages=my_default_errors_email
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',
                  'is_student', 'is_teacher', 'is_admin')

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
             attrs={'id' :'name' ,'type':'name' ,'name':'name', 'placeholder':'الاسم'}
        ),
    )
    email = forms.EmailField(
        widget=forms.TextInput(
             attrs={ 'id' :'email' ,'type':'email' ,'name':'email', 'placeholder':'البريد الالكتروني'}
        ),
    )
    desc = forms.CharField(
        widget=forms.Textarea(
             attrs={'id':'desc','name':'desc', 'placeholder':'محتوى الرسالة'}
        ),
    )
    class Meta:
        model = Contact
        fields = ('name','email','desc')
    