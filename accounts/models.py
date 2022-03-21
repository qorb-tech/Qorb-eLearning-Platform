from operator import mod
from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.EmailField(max_length=120)
    desc = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


def student_directory_path(inst, file_name):
    return f'student_profile_images/{inst.user}/{file_name}'


def teacher_directory_path(inst, file_name):
    return f'teacher_profile_images/{inst.user}/{file_name}'


User = get_user_model()

class Profile(models.Model):
    INTEREST_CHOICES = (
        ("programming", "Programming"),
        ("testing", "Testing"),
        ("control", 'Control'),
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=122, null=True, blank=True)
    intersted_with = models.CharField(
        max_length=11, default='programming', choices=INTEREST_CHOICES)
    email = models.EmailField(null=True, blank=True)
  
    def __str__(self):
        return self.user.username


class Student(Profile):
    avatar = models.ImageField(
        default='student_profile_images/default.png', upload_to=student_directory_path)

    class Meta:
        verbose_name = ('Student Profile')

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Teacher(Profile):
    avatar = models.ImageField(
        default='teacher_profile_images/default.png', upload_to=teacher_directory_path)

    class Meta:
        verbose_name = ('Teacher Profile')

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
