from rest_framework import (
    generics,
    permissions,
)
from westudy.models import Modality
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from westudy.permissions import RegisterWithoutAuthPermission, IsAdminUser

from .serializers import (
    ModalitySerializer,
)

class ModalityCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = ModalitySerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'message': 'Modality created'}
        return response

class ModalityListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = ModalitySerializer

    def get_queryset(self):
        return Modality.objects.all()


class ModalityDetailView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = ModalitySerializer

    def get_object(self):
        modality_id = self.kwargs.get('id')
        try:
            modality = Modality.objects.get(id=modality_id)
        except Modality.DoesNotExist:
            raise serializers.ValidationError('Modality not found')
        return modality


class ModalityUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = ModalitySerializer

    def get_object(self):
        modality_id = self.kwargs.get('id')
        try:
            modality = Modality.objects.get(id=modality_id)
        except Modality.DoesNotExist:
            raise serializers.ValidationError('Modality not found')
        return modality

    def update(self, request, *args, **kwargs):
            modality = self.get_object()
            serializer = self.get_serializer(modality, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Modality updated'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ModalityDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = ModalitySerializer

    def get_queryset(self):
        modality_id = self.kwargs.get('id')
        try:
            modality = Modality.objects.get(id=modality_id)
            return modality
        except Modality.DoesNotExist:
            raise serializers.ValidationError('Modality not found')

    def delete(self, request, *args, **kwargs):
        modality = self.get_queryset()
        modality.delete()
        return Response({'message': 'Modality deleted'}, status=status.HTTP_200_OK)