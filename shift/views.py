from rest_framework import (
    generics,
    permissions,
)
from westudy.models import University, Shifts, Course, Schedule
from rest_framework.response import Response
from rest_framework import status, serializers
from westudy.permissions import RegisterWithoutAuthPermission, IsAdminUser, IsUniversityAdmin
from datetime import datetime, time
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.views import APIView
from .serializers import (
    ShiftSerializer
)

class ShiftListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = ShiftSerializer

    def get_queryset(self):
        course_id = self.kwargs.get('id')
        user = self.request.user
        try:
            course = Course.objects.get(id=course_id)
            if isinstance(user, University):
                return Shifts.objects.filter(course=course,id_university=user.id)
            else:
                return Shifts.objects.filter(course=course)
        except Course.DoesNotExist:
            raise serializers.ValidationError('Course not found')

class ShiftCreateView(generics.CreateAPIView):
    permission_classes = [IsUniversityAdmin]  # Permisos
    serializer_class = ShiftSerializer

    def create(self, request, *args, **kwargs):
        course_id = self.kwargs.get('id')
        user = self.request.user
        if isinstance(user, University):
            queryset = Course.objects.filter(university=user)
        else:
            queryset = Course.objects.all()
        try:
            course = queryset.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError('Course not found')
        start_time_str = request.data.get('start_time')
        end_time_str = request.data.get('end_time')

        # Convertir las cadenas de texto a objetos datetime.time
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()

        if start_time >= end_time:
            raise serializers.ValidationError('La hora de inicio debe ser menor a la hora de fin')
        
        if start_time == end_time:
            raise serializers.ValidationError('La hora de inicio debe ser diferente a la hora de fin')
        
        if Shifts.objects.filter(course=course, start_time=start_time, end_time=end_time).exists():
            raise serializers.ValidationError('Ya existe un turno con esas horas')


        # Crear una lista para almacenar los nombres de los turnos
        shift_names = set()

        # Verificar si el turno de inicio está en la madrugada
        if time(0, 0) <= start_time <= time(4, 59):
            shift_names.add('Madrugada')

        # Verificar si el turno de inicio está en la mañana
        if time(5, 0) <= start_time <= time(11, 59):
            shift_names.add('Mañana')

        # Verificar si el turno de inicio está en la tarde
        if time(12, 0) <= start_time <= time(18, 59):
            shift_names.add('Tarde')

        # Verificar si el turno de inicio está en la noche
        if time(19, 0) <= start_time <= time(23, 59):
            shift_names.add('Noche')

        # Verificar si el turno de fin está en la madrugada y no se encuentra en el turno de inicio
        if time(0, 0) <= end_time <= time(4, 59) and 'Madrugada' not in shift_names:
            shift_names.add('Madrugada')

        # Verificar si el turno de fin está en la mañana y no se encuentra en el turno de inicio
        if time(5, 0) <= end_time <= time(11, 59) and 'Mañana' not in shift_names:
            shift_names.add('Mañana')

        # Verificar si el turno de fin está en la tarde y no se encuentra en el turno de inicio
        if time(12, 0) <= end_time <= time(18, 59) and 'Tarde' not in shift_names:
            shift_names.add('Tarde')

        # Verificar si el turno de fin está en la noche y no se encuentra en el turno de inicio
        if time(19, 0) <= end_time <= time(23, 59) and 'Noche' not in shift_names:
            shift_names.add('Noche')

        # Unir los nombres de los turnos en una cadena de texto separada por guiones
        if len(shift_names) > 0:
            name = ' - '.join(sorted(shift_names))
        else:
            return Response({'message': 'Invalid shift'}, status=status.HTTP_400_BAD_REQUEST)
        
        shift_Schedule = name.split(" - ")

        for shift_name in shift_Schedule:
            if not Schedule.objects.filter(name=shift_name, course=course).exists():
                Schedule.objects.create(name=shift_name, course=course)
        
    
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course, shift=name, id_university=user.id)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Shift created'}, status=status.HTTP_201_CREATED, headers=headers)


class ShiftDeleteView(generics.DestroyAPIView):
    """ Delete a course """
    permission_classes = [IsUniversityAdmin]  # Permisos
    serializer_class = ShiftSerializer

    def delete(self, request, *args, **kwargs):
        shift_id = self.kwargs.get('id')
        shift = generics.get_object_or_404(Shifts, id=shift_id)
        course = generics.get_object_or_404(Course, id=shift.course.id)
        count = {"Mañana": 0, "Tarde": 0, "Noche": 0, "Madrugada": 0}
        shift_Schedule_list = shift.shift.split(" - ")
        for shift in Shifts.objects.filter(course=course):
            shift_Schedule = shift.shift.split(" - ")
            for shift_name in shift_Schedule:
                if shift_name in shift_Schedule_list:
                    if shift_name in count:
                        count[shift_name] += 1
        for shift_name in shift_Schedule_list:
            if count[shift_name]:
                Schedule.objects.filter(name=shift_name, course=course).delete()
        shift.delete()
        return Response({'message': 'Course deleted'}, status=status.HTTP_200_OK)