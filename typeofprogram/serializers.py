from django.utils.translation import gettext as _ # This is used to translate the error messages
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from westudy.models import TypeOfProgram

class TypeOfProgramCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeOfProgram
        fields = ('id', 'name', )
        read_only_fields = ('id',)


class TypeOfProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeOfProgram
        fields = ('id', 'name','number_of_courses',)
        read_only_fields = ('id',)
