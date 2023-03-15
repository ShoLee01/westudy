from rest_framework import (
    generics,
    permissions,
)
from westudy.models import University
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from westudy.permissions import RegisterWithoutAuthPermission, IsAdminUser
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    UniversitySerializer
)

class UniversityListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission]  # Permisos
    serializer_class = UniversitySerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        return University.objects.all()

class UniversityGetView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission]  # Permisos
    serializer_class = UniversitySerializer

    def get_object(self):
        university_id = self.kwargs.get('id')
        university = get_object_or_404(University, id=university_id)
        return university
        


class UniversityCreateView(generics.CreateAPIView):
    """ Create a new university """
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = UniversitySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'University created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UniversityUpdateView(generics.UpdateAPIView):
    """ Update a university """
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = UniversitySerializer

    def get_object(self):
        university_id = self.kwargs.get('id')
        try:
            university = University.objects.get(id=university_id)
        except University.DoesNotExist:
            raise Response({'message': 'University not found'}, status=status.HTTP_404_NOT_FOUND)
        return university

    def update(self, request, *args, **kwargs):
        university = self.get_object()
        print(university)
        serializer = self.get_serializer(university, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'University updated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UniversityDeleteView(generics.DestroyAPIView):
    """ Delete a university """
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = UniversitySerializer

    def delete(self, request, *args, **kwargs):
        university_id = self.kwargs.get('id')
        university = University.objects.filter(id=university_id)
        if university.exists():
            university.delete()
            return Response({'message': 'University deleted'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'University not found'}, status=status.HTTP_404_NOT_FOUND)
    