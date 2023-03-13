from rest_framework import (
    generics,
    permissions,
)
from westudy.models import Category
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from westudy.permissions import RegisterWithoutAuthPermission, IsAdminUser

from .serializers import (
    CategorySerializer,
    CategoryCreateSerializer
)

class CategoryCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = CategoryCreateSerializer

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'message': 'Category created'}
        return response

class CategoryListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


class CategoryDetailView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = CategorySerializer

    def get_object(self):
        category_id = self.kwargs.get('id')
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError('Category not found')
        return category

class CategoryUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = CategorySerializer

    def get_object(self):
        category_id = self.kwargs.get('id')
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError('Category not found')
        return category

    def update(self, request, *args, **kwargs):
            category = self.get_object()
            serializer = self.get_serializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Category updated'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = CategorySerializer

    def get_queryset(self):
        category_id = self.kwargs.get('id')
        try:
            category = Category.objects.get(id=category_id)
            return category
        except Category.DoesNotExist:
            raise serializers.ValidationError('Category not found')

    def delete(self, request, *args, **kwargs):
        category = self.get_queryset()
        category.delete()
        return Response({'message': 'Category deleted'}, status=status.HTTP_200_OK)