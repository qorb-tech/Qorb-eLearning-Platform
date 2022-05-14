# Generated by Django 3.2.5 on 2022-02-21 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0012_alter_quiz_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='course',
        ),
        migrations.AddField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teacher.course'),
        ),
    ]
