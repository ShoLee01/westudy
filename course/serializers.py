from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _ # This is used to translate the error messages
from rest_framework import serializers
from westudy.models import Course, Shifts
from shift.serializers import (
    ShiftSerializer
)

class CourseSerializer(serializers.ModelSerializer):
    shifts = ShiftSerializer(many=True, read_only=True)
    shifts_summary = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id', 'title','link','numer_of_months', 'background_image', 'institution', 'requirements','number_of_stars',
            'start_of_course', 'end_of_course', 'discount', 'price',
            'country', 'city', 'registration_date', 'language', 'number_of_teachers', 'accept_installments',
            'category', 'type_of_program','modality',  # Incluir las relaciones muchos a muchos
            'shifts', 'shifts_summary'  # Añade los turnos (Shifts) aquí
        )
        read_only_fields = ('id',)
        depth = 1  # Indicar el nivel de profundidad deseado en las relaciones

    def get_shifts_summary(self, obj):
        shifts = Shifts.objects.filter(course=obj)
        list_shift = []
        for element in shifts:
            list_shift += element.shift.split(' - ')
        list_shift = list(set(list_shift))  # Eliminar duplicados
        shifts_summary = ', '.join(list_shift)
        return shifts_summary


class CourseCreateSerializer(serializers.ModelSerializer):
    """Serializer for the Category objects"""
    #background_image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = Course
        fields = ('id', 'title','link','numer_of_months', 'registration_date','requirements', 'start_of_course', 'end_of_course', 'discount', 'price', 'country', 'city', 'language', 'number_of_teachers', 'accept_installments',)
        read_only_fields = ('id',)