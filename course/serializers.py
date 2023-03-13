from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _ # This is used to translate the error messages
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from westudy.models import Course, Category
from drf_extra_fields.fields import Base64ImageField

class CourseSerializer(serializers.ModelSerializer):
    """Serializer for the Category objects"""
    background_image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = Course
        fields = ('id', 'title', 'program_type', 'background_image', 'institution', 'requirements', 'start_of_course', 'end_of_course', 'start_time', 'completion_time', 'discount', 'price', 'country', 'city', 'language', 'number_of_teachers', 'accept_installments',)
        read_only_fields = ('id',)

class CourseCreateSerializer(serializers.ModelSerializer):
    """Serializer for the Category objects"""
    background_image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = Course
        fields = ('id', 'title', 'program_type', 'background_image', 'requirements', 'start_of_course', 'end_of_course', 'start_time', 'completion_time', 'discount', 'price', 'country', 'city', 'language', 'number_of_teachers', 'accept_installments',)
        read_only_fields = ('id',)