# Generated by Django 3.2.5 on 2022-02-21 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0013_auto_20220221_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='text',
        ),
        migrations.AddField(
            model_name='answer',
            name='option1',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='option2',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='option3',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='option4',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]