from rest_framework import (
    generics,
    permissions,
)
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import (
    authenticate,
)
from django.http import Http404
import logging
from django.contrib.auth.hashers import make_password
from westudy.models import University, User
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import status
from westudy.permissions import RegisterWithoutAuthPermission, IsAdminUser, IsUniversityAdmin
from rest_framework.pagination import PageNumberPagination
from app import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from westudy.tokens import UniversityTokenObtainPairSerializer
import boto3
from .serializers import (
    UniversitySerializer, UniversitySerializerBasic, 
    UniversitySerializerCode, UniversityRegisteredAccounts,
    UniversityRegisterCreate
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
    

class UniversityRegisteredAccountsView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission]  # Permisos
    serializer_class = UniversityRegisteredAccounts

    def create(self, request, *args, **kwargs):
        university_email = request.data.get('email')
        try:
            university = University.objects.get(email=university_email)
            return Response({'message': 'University exists', 'university': True}, status=status.HTTP_200_OK)
        except University.DoesNotExist:
            return Response({'message': 'University not found', 'university': False}, status=status.HTTP_200_OK)

    
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
    serializer_class = UniversityRegisterCreate

    def perform_create(self, serializer):
        if serializer.is_valid():
            instance = serializer.save()
            return instance
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        instance = self.perform_create(serializer)
        if isinstance(instance, Response):
            return instance
        headers = self.get_success_headers(serializer.data)
        response_data = {'message': 'University created', 'university_id': instance.id}
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


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
        if 'password' in request.data:
            # Cifra la contraseña según la contraseña ingresada
            encrypted_password = make_password(request.data['password'])
            request.data['password'] = encrypted_password
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
        #logging.basicConfig(level=logging.DEBUG)

        #session = boto3.Session(
                #aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                #aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                #region_name=settings.AWS_S3_REGION_NAME
            #)
        #s3 = session.resource('s3')
        #bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        #bucket.Object(university.background_image.name).delete()
        #bucket.Object(university.logo.name).delete()
        # Elimina el objeto del modelo de la base de datos
        university.delete()
        return Response({'message': 'University deleted'}, status=status.HTTP_200_OK)

        

class InactiveUniversitiesView(generics.ListAPIView):
    queryset = University.objects.filter(is_active=False)
    serializer_class = UniversitySerializerCode
    permission_classes = [IsAdminUser]  # Permisos
        
class UniversityActivateView(generics.CreateAPIView):
    """ Activate a university """
    authentication_classes = []
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
                return Response({'message': 'Invalid activation code'}, status=status.HTTP_200_OK)

            if university.is_active:
                return Response({'message': 'University is already active'}, status=status.HTTP_200_OK)

            university.is_active = True
            university.save()

            return Response({'message': 'University activated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(TokenObtainPairView):
    serializer_class = UniversityTokenObtainPairSerializer