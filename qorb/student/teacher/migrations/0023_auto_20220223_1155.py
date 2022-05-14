# Generated by Django 3.2.12 on 2022-02-23 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0022_auto_20220223_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizstudent',
            name='done_or_not',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]