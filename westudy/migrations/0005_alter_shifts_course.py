# Generated by Django 4.1.5 on 2023-05-16 03:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("westudy", "0004_course_numer_of_months"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shifts",
            name="course",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shifts",
                to="westudy.course",
            ),
        ),
    ]
