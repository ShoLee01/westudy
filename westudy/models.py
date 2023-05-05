from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import (
    AbstractBaseUser,
     BaseUserManager,
    PermissionsMixin,
)

import uuid

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        if not email: # If email is not provided 
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields) # Normalize email
        user.set_password(password) # Set password
        user.save(using=self._db) # Save user

        return user


    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db) # ._db meaning the database that is being used

        return user
    
class TypeOfProgram(models.Model):
    name = models.CharField(max_length=100, null=False)
    number_of_courses = models.IntegerField(null=True, default=0)
    
    def __str__(self):
        return self.name
class Modality(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)
    number_of_courses = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name

class University(models.Model):
    email = models.EmailField(max_length=100, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    name = models.CharField(max_length=100, null=False)
    activation_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    background_image = models.ImageField(blank='', default="", upload_to='background/',null=True)
    verified = models.BooleanField(default=False, null=True)
    global_ranking = models.IntegerField(null=True)
    national_level_ranking = models.IntegerField(null=True)
    latin_american_ranking = models.IntegerField(null=True)
    is_active = models.BooleanField(default=False)
    number_of_courses = models.IntegerField(default=0)
    country = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    logo = models.ImageField(blank='', default="", upload_to='logo/',null=True)
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.set_password(self.password)
        super(University, self).save(*args, **kwargs)

class Course(models.Model):
    title = models.CharField(max_length=100, null=False)
    link = models.TextField(null=True)
    background_image = models.ImageField(blank='', default="", upload_to='background/',null=True)
    institution = models.CharField(max_length=100, null=False)
    requirements = models.BooleanField(default=False)
    number_of_stars = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
    start_of_course = models.DateField(null=True)
    end_of_course = models.DateField(null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    country = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    registration_date = models.DateField(null=True)
    language = models.CharField(max_length=100, null=False)
    number_of_teachers = models.IntegerField(null=True)
    accept_installments = models.BooleanField(default=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, null=True)
    category = models.ManyToManyField(Category, related_name='category')
    modality = models.ManyToManyField(Modality, related_name='modality')
    type_of_program = models.ManyToManyField(TypeOfProgram, related_name='type_of_program')
    def __str__(self):
        return self.title
    
class Shifts(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    id_university = models.IntegerField(null=False, default=0)
    shift = models.CharField(max_length=100, null=True)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)

    def __str__(self):
        return self.name

class User(AbstractBaseUser, PermissionsMixin):
        profile = models.ImageField(blank='', default="", upload_to='profile/',null=True)
        names = models.CharField(max_length=100)
        surnames = models.CharField(max_length=100)
        email = models.EmailField(max_length=100, unique=True)
        nationality = models.CharField(max_length=100)
        date_of_birth = models.DateField(null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)
        saved_courses = models.ManyToManyField(Course, related_name='saved_courses')
        program_preferences = models.ManyToManyField(TypeOfProgram, related_name='program_preferences')

        objects = UserManager()

        USERNAME_FIELD = 'email' # This is the field that will be used to login


