from rest_framework import (
    generics,
    permissions,
)
from westudy.models import Schedule, Course
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from westudy.permissions import RegisterWithoutAuthPermission, IsAdminUser

from .serializers import (
    ScheduleSerializer
)

class ScheduleCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = ScheduleSerializer

    def perform_create(self, serializer):
        course_id = self.kwargs.get('id')
        try:
            course = Course.objects.get(id=course_id)
            serializer.save(course=course)
            return Response({'message': 'Schedule created'}, status=status.HTTP_201_CREATED)
        except Course.DoesNotExist:
            raise serializers.ValidationError('Course not found')


class ScheduleListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission]  # Permisos
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

class ScheduleGetView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission]  # Permisos
    serializer_class = ScheduleSerializer

    def get_object(self):
        schedule_id = self.kwargs.get('id')
        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            raise serializers.ValidationError('Schedule not found')
        return schedule

class ScheduleUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = ScheduleSerializer

    def get_object(self):
        schedule_id = self.kwargs.get('id')
        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            raise serializers.ValidationError('Schedule not found')
        return schedule

    def update(self, request, *args, **kwargs):
        schedule = self.get_object()
        print(schedule)
        serializer = self.get_serializer(schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Schedule updated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = ScheduleSerializer

    def get_object(self):
        schedule_id = self.kwargs.get('id')
        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            raise serializers.ValidationError('Schedule not found')
        return schedule

    def delete(self, request, *args, **kwargs):
        schedule = self.get_object()
        schedule.delete()
        return Response({'message': 'Schedule deleted'}, status=status.HTTP_200_OK)


class ScheduleListCourseView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission]  # Permisos
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        course_id = self.kwargs.get('id')
        try:
            course = Course.objects.get(id=course_id)
            queryset = Schedule.objects.filter(course=course)
        except Course.DoesNotExist:
            raise serializers.ValidationError('Course not found')
        return queryset