from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _ # This is used to translate the error messages
from rest_framework import serializers
import uuid
from django.core.exceptions import ValidationError
from university.university_tokens import UniversityAccessToken
from westudy.models import University
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
""" from drf_extra_fields.fields import Base64ImageField """


class UniversitySerializerBasic(serializers.ModelSerializer):
    """Serializer for university objects"""

    class Meta:
        model = University
        fields = ['name', 'background_image', 'global_ranking', 'national_level_ranking', 'latin_american_ranking', 'country', 'city', 'logo']
        read_only_fields = ('id',)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


class UniversitySerializer(serializers.ModelSerializer):
    """Serializer for university objects"""
    # background_image = Base64ImageField(required=False, allow_null=True)
    # logo = Base64ImageField(required=False, allow_null=True) 
    class Meta: 
        model = University
        fields = ['id','email', 'name', 'password', 'background_image', 'verified', 'global_ranking', 'national_level_ranking', 'latin_american_ranking', 'number_of_courses', 'country', 'city', 'logo']
        read_only_fields = ('id',)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


class UniversitySerializerCode(serializers.ModelSerializer):
    activation_code = serializers.CharField(required=True)

    class Meta:
        model = University
        fields = ['name', 'activation_code']
        read_only_fields = ('name',)

    def validate_activation_code(self, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValidationError('Invalid UUID format')
        return value



