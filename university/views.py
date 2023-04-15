from rest_framework import (
    generics,
    permissions,
)
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import (
    authenticate,
)
from westudy.models import University, User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import status
from westudy.permissions import RegisterWithoutAuthPermission, IsAdminUser, IsUniversityAdmin
from rest_framework.pagination import PageNumberPagination

from rest_framework_simplejwt.views import TokenObtainPairView
from westudy.tokens import UniversityTokenObtainPairSerializer

from .serializers import (
    UniversitySerializer, UniversitySerializerBasic, UniversitySerializerCode
)

class UniversityListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission]  # Permisos
    serializer_class = UniversitySerializerBasic
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        return University.objects.all()

class UniversityGetView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission]  # Permisos
    serializer_class = UniversitySerializerBasic

    def get_object(self):
        university_id = self.kwargs.get('id')
        university = get_object_or_404(University, id=university_id)
        return university
    
class UniversityGetLoginView(generics.RetrieveAPIView):
    permission_classes = [IsUniversityAdmin]  # Permisos
    serializer_class = UniversitySerializer

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, User) and user.is_superuser:
            return University.objects.all()
        elif isinstance(user, University):
            return University.objects.filter(id=user.id)

    def get_object(self):
        queryset = self.get_queryset()
        print(queryset)
        university_id = self.kwargs.get('id')
        university = get_object_or_404(queryset, id=university_id)
        return university
        


class UniversityCreateView(generics.CreateAPIView):
    """ Create a new university """
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission]  # Permisos
    serializer_class = UniversitySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'University created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UniversityUpdateView(generics.UpdateAPIView):
    permission_classes = [IsUniversityAdmin]  # Permisos
    serializer_class = UniversitySerializer

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, University):
            return University.objects.filter(id=user.id)
        else:
            return University.objects.all()
            
    def get_object(self):
        queryset = self.get_queryset()
        university_id = self.kwargs.get('id')
        university = generics.get_object_or_404(queryset, id=university_id)
        return university

    def update(self, request, *args, **kwargs):
        university = self.get_object()
        serializer = self.get_serializer(university, data=request.data, partial=True)

        if serializer.is_valid():
            if 'password' in request.data:
                university.set_password(request.data['password'])

            serializer.save()
            return Response({'message': 'University updated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UniversityDeleteView(generics.DestroyAPIView):
    """ Delete a university """
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = UniversitySerializer

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, University):
            return University.objects.filter(id=user.id)
        else:
            return University.objects.all()
            
    def get_object(self):
        queryset = self.get_queryset()
        university_id = self.kwargs.get('id')
        university = generics.get_object_or_404(queryset, id=university_id)
        return university

    def delete(self, request, *args, **kwargs):
        university = self.get_object()
        if university.exists():
            university.delete()
            return Response({'message': 'University deleted'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'University not found'}, status=status.HTTP_404_NOT_FOUND)
        

class InactiveUniversitiesView(generics.ListAPIView):
    queryset = University.objects.filter(is_active=False)
    serializer_class = UniversitySerializerCode
    permission_classes = [IsAdminUser]  # Permisos
        
class UniversityActivateView(generics.CreateAPIView):
    """ Activate a university """
    permission_classes = [RegisterWithoutAuthPermission]  # Permisos
    serializer_class = UniversitySerializerCode
    queryset = University.objects.all()

    def create(self, request, *args, **kwargs):
        print(request.data)  # Agregue esta línea para verificar los datos enviados en la solicitud
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            activation_code = serializer.validated_data['activation_code']
            try:
                university = University.objects.get(activation_code=activation_code)
            except University.DoesNotExist:
                return Response({'message': 'Invalid activation code'}, status=status.HTTP_404_NOT_FOUND)

            if university.is_active:
                return Response({'message': 'University is already active'}, status=status.HTTP_400_BAD_REQUEST)

            university.is_active = True
            university.save()

            return Response({'message': 'University activated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(TokenObtainPairView):
    serializer_class = UniversityTokenObtainPairSerializer