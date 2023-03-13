# Generated by Django 4.1.5 on 2023-01-29 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("westudy", "0002_alter_user_date_of_birth"),
    ]

    operations = [
        migrations.CreateModel(
            name="Unisersity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "background_image",
                    models.ImageField(
                        blank="", default="", null=True, upload_to="background/"
                    ),
                ),
                ("verified", models.BooleanField(default=False, null=True)),
                ("global_ranking", models.IntegerField(null=True)),
                ("national_level_ranking", models.IntegerField(null=True)),
                ("latin_american_ranking", models.IntegerField(null=True)),
                ("number_of_courses", models.IntegerField(default=0)),
                ("country", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                (
                    "logo",
                    models.ImageField(
                        blank="", default="", null=True, upload_to="logo/"
                    ),
                ),
            ],
        ),
    ]
