# Generated by Django 4.1.5 on 2023-02-03 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("westudy", "0009_course_link"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="course_modalities",
        ),
    ]
