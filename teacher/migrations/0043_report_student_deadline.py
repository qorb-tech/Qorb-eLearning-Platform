# Generated by Django 3.2.12 on 2022-03-21 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0042_report_student_last_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='report_student',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
