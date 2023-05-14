from rest_framework import (
    generics,
    permissions,
)
from westudy.models import TypeOfProgram, User
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from westudy.permissions import RegisterWithoutAuthPermission, IsAdminUser

from .serializers import (
    TypeOfProgramSerializer,
    TypeOfProgramCreateSerializer
)

class TypeOfProgramCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = TypeOfProgramCreateSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'message': 'Type of program created'}
        return response

class TypeOfProgramListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = TypeOfProgramSerializer

    def get_queryset(self):
        return TypeOfProgram.objects.all().order_by('name')


class TypeOfProgramDetailView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = TypeOfProgramSerializer

    def get_object(self):
        type_of_program_id = self.kwargs.get('id')
        try:
            type_of_program = TypeOfProgram.objects.get(id=type_of_program_id)
        except TypeOfProgram.DoesNotExist:
            raise serializers.ValidationError('Type of program not found')
        return type_of_program


class TypeOfProgramUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = TypeOfProgramSerializer

    def get_object(self):
        type_of_program_id = self.kwargs.get('id')
        try:
            type_of_program = TypeOfProgram.objects.get(id=type_of_program_id)
        except TypeOfProgram.DoesNotExist:
            raise serializers.ValidationError('Type of program not found')
        return type_of_program

    def update(self, request, *args, **kwargs):
            type_of_program = self.get_object()
            serializer = self.get_serializer(type_of_program, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Type of program updated'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TypeOfProgramDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = TypeOfProgramSerializer

    def get_queryset(self):
        type_of_program_id = self.kwargs.get('id')
        try:
            type_of_program = TypeOfProgram.objects.get(id=type_of_program_id)
            return type_of_program
        except TypeOfProgram.DoesNotExist:
            raise serializers.ValidationError('Type of program not found')

    def delete(self, request, *args, **kwargs):
        type_of_program = self.get_queryset()
        type_of_program.delete()
        return Response({'message': 'Type of program deleted'}, status=status.HTTP_200_OK)


class PreferredByUsersView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    
    def get(self, request, *args, **kwargs):
        type_of_program_name = self.kwargs.get('name')
        try:
            number_of_people_following = TypeOfProgram.objects.get(name=type_of_program_name).program_preferences.count()
        except TypeOfProgram.DoesNotExist:
            return Response({'error': 'Type of program not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'number_of_people_following': number_of_people_following}, status=status.HTTP_200_OK)

