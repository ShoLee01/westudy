from django.utils.translation import gettext as _ # This is used to translate the error messages
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from westudy.models import Shifts

class ShiftSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shifts
        fields = ('id', 'shift', 'weekday', 'start_time', 'end_time','id_university',)
        read_only_fields = ('id','shift','id_university')