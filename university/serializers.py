from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _ # This is used to translate the error messages
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from westudy.models import University
""" from drf_extra_fields.fields import Base64ImageField """


class UniversitySerializer(serializers.ModelSerializer):
    """Serializer for university objects"""
    # background_image = Base64ImageField(required=False, allow_null=True)
    # logo = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = University
        fields = "__all__"
        read_only_fields = ('id',)

    def list(self, request):
        queryset = University.objects.all()
        print(queryset)
        serializer = UniversitySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, validated_data):
        """Create a new university"""
        university = University.objects.create(**validated_data)
        if university:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

