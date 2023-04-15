# Generated by Django 4.1.5 on 2023-04-13 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("westudy", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="number_of_stars",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=10, null=True
            ),
        ),
    ]