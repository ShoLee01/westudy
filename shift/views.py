from rest_framework import (
    generics,
    permissions,
)
from rest_framework.views import APIView
from westudy.models import University, Shifts, Course
from rest_framework.response import Response
from rest_framework import status, serializers
from westudy.permissions import RegisterWithoutAuthPermission, IsAdminUser, IsUniversityAdmin
from rest_framework.renderers import JSONRenderer
from datetime import datetime
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

""" class ShiftByCourseListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = ShiftSerializer
    
    def get_queryset(self):
        course_id = self.kwargs.get('id')
        user = self.request.user
        try:
            course = Course.objects.get(id=course_id)
            if isinstance(user, University):
                queryset = Shifts.objects.filter(course=course, id_university=user.id)
            else:
                queryset = Shifts.objects.filter(course=course)
            list_shift = []
            for element in queryset:
                list_shift.append(element.shift)
            list_shift = set(list_shift)
            shifts = ', '.join(list_shift)
            response_data = {"shifts": shifts}
            response = Response(response_data, status=status.HTTP_200_OK)
            return JSONRenderer().render(response.data)  # Renderizar el contenido de la respuesta antes de devolverla
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND) """
        
class ShiftByCourseListView(APIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission]

    def get(self, request, id):
        course_id = id
        user = self.request.user
        try:
            course = Course.objects.get(id=course_id)
            if isinstance(user, University):
                queryset = Shifts.objects.filter(course=course, id_university=user.id)
            else:
                queryset = Shifts.objects.filter(course=course)
            list_shift = []
            for element in queryset:
                list_shift += element.shift.split(' - ')
            list_shift = list(set(list_shift))  # Eliminar duplicados
            shifts = ', '.join(list_shift)
            response_data = {"shifts": shifts}
            return Response(response_data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)



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


        madrugada_inicio = datetime.strptime('00:00:00', '%H:%M:%S').time()
        madrugada_fin = datetime.strptime('04:59:59', '%H:%M:%S').time()
        manana_inicio = datetime.strptime('05:00:00', '%H:%M:%S').time()
        manana_fin = datetime.strptime('11:59:59', '%H:%M:%S').time()
        tarde_inicio = datetime.strptime('12:00:00', '%H:%M:%S').time()
        tarde_fin = datetime.strptime('18:59:59', '%H:%M:%S').time()
        noche_inicio = datetime.strptime('19:00:00', '%H:%M:%S').time()
        noche_fin = datetime.strptime('23:59:59', '%H:%M:%S').time()

        # Determinar el turno correspondiente
        shift_names = set()
        if madrugada_inicio <= start_time <= madrugada_fin and madrugada_inicio <= end_time <= madrugada_fin:
            shift_names.add("Madrugada - Madrugada")
        if manana_inicio <= start_time <= manana_fin and manana_inicio <= end_time <= manana_fin:
            shift_names.add("Mañana - Mañana")
        if tarde_inicio <= start_time <= tarde_fin and tarde_inicio <= end_time <= tarde_fin:
            shift_names.add("Tarde")
        if noche_inicio <= start_time <= noche_fin and noche_inicio <= end_time <= noche_fin:
            shift_names.add("Noche - Noche")
        if start_time <= manana_fin and end_time >= tarde_inicio:
            shift_names.add("Mañana - Tarde")
        if start_time <= tarde_fin and end_time >= noche_inicio:
            shift_names.add("Tarde - Noche")
        if (start_time >= noche_inicio or end_time <= madrugada_fin) and ("Noche - Madrugada" not in shift_names):
            shift_names.add("Noche - Madrugada")
        if madrugada_inicio <= start_time <= madrugada_fin and manana_inicio <= end_time <= manana_fin:
            shift_names.add("Madrugada - Mañana")

        # Unir los nombres de los turnos en una cadena de texto separada por guiones
        if len(shift_names) > 0:
            name = ' - '.join(sorted(shift_names))
        else:
            return Response({'message': 'Invalid shift'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course, shift=name, id_university=user.id)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Shift created'}, status=status.HTTP_201_CREATED, headers=headers)


class ShiftDeleteView(generics.DestroyAPIView):
    """ Delete a course """
    permission_classes = [IsUniversityAdmin]  # Permisos
    serializer_class = ShiftSerializer

    def get_queryset(self):
        shift_id = self.kwargs.get('id')
        user = self.request.user
        try:
            if isinstance(user, University):
                return Shifts.objects.filter(id=shift_id, id_university=user.id)
            else:
                return Shifts.objects.filter(id=shift_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError('Course not found')

    def delete(self, request, *args, **kwargs):
        shift = self.get_queryset()
        shift.delete()
        return Response({'message': 'Course deleted'}, status=status.HTTP_200_OK)