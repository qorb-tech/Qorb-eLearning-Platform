# Generated by Django 3.2.12 on 2022-03-21 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0041_auto_20220321_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='report_student',
            name='last_modified',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
