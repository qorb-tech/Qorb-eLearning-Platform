# Generated by Django 3.2.12 on 2022-02-17 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('teacher', '0005_degrees'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Degrees',
            new_name='Degree',
        ),
        migrations.RenameModel(
            old_name='Reports',
            new_name='Report',
        ),
    ]
