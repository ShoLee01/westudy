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
    """Serializer for the Course objects"""
    #background_image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Course
        fields = (
            'id', 'title','link', 'background_image', 'institution', 'requirements','number_of_stars',
            'start_of_course', 'end_of_course', 'discount', 'price',
            'country', 'city', 'registration_date', 'language', 'number_of_teachers', 'accept_installments',
            'category', 'type_of_program','modality'  # Incluir las relaciones muchos a muchos
        )
        read_only_fields = ('id',)
        depth = 1  # Indicar el nivel de profundidad deseado en las relaciones


class CourseCreateSerializer(serializers.ModelSerializer):
    """Serializer for the Category objects"""
    #background_image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = Course
        fields = ('id', 'title','link', 'background_image','numer_of_months', 'registration_date','requirements', 'start_of_course', 'end_of_course', 'discount', 'price', 'country', 'city', 'language', 'number_of_teachers', 'accept_installments',)
        read_only_fields = ('id',)