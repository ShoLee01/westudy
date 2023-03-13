from rest_framework import (
    generics,
    permissions,
)
from functools import reduce
from django.shortcuts import get_object_or_404
from westudy.models import Course, University, Modality, Category, TypeOfProgram
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers
from westudy.permissions import RegisterWithoutAuthPermission, IsAdminUser
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    CourseSerializer,
    CourseCreateSerializer
)

class CourseCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = CourseCreateSerializer

    def perform_create(self, serializer):
        university_id = self.kwargs.get('id')
        try:
            university = University.objects.get(id=university_id)
            serializer.save(university=university,institution=university.name)
            return Response({'message': 'Course created'}, status=status.HTTP_201_CREATED)
        except University.DoesNotExist:
            raise serializers.ValidationError('University not found')

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {'message': 'Course created'}
        return response

class CourseListByUniversityView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = CourseSerializer

    def get_queryset(self):
        university_id = self.kwargs.get('id')
        try:
            university = University.objects.get(id=university_id)
            return Course.objects.filter(university=university)
        except University.DoesNotExist:
            raise serializers.ValidationError('University not found')

class CourseListView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        return Course.objects.all()

class CourseDetailView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = CourseSerializer

    def get_object(self):
        course_id = self.kwargs.get('id')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError('Course not found')
        return course

class CourseUpdateView(generics.UpdateAPIView):
    """ Update a course """
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = CourseSerializer

    def get_object(self):
        course_id = self.kwargs.get('id')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError('Course not found')
        return course

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Course updated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class CourseDeleteView(generics.DestroyAPIView):
    """ Delete a course """
    permission_classes = [IsAdminUser]  # Permisos
    serializer_class = CourseSerializer

    def get_object(self):
        course_id = self.kwargs.get('id')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError('Course not found')
        return course

    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        course.delete()
        return Response({'message': 'Course deleted'}, status=status.HTTP_200_OK)


# Relationships


class CategoryAssignmentSerializer(APIView):
    permission_classes = [IsAdminUser]  # Permisos

    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        category_id = kwargs.get('category_id')
        course = get_object_or_404(Course, id=course_id)
        category = get_object_or_404(Category, id=category_id)
        if category in course.category.all():
            return Response({'message': 'Category already assigned'}, status=status.HTTP_400_BAD_REQUEST)
        course.category.add(category)
        category.number_of_courses += 1
        category.save()
        return Response({'message': 'Category assigned'}, status=status.HTTP_201_CREATED)

class ModalityAssignmentSerializer(APIView):
    permission_classes = [IsAdminUser]  # Permisos

    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        modality_id = kwargs.get('modality_id')
        course = get_object_or_404(Course, id=course_id)
        modality = get_object_or_404(Modality, id=modality_id)
        if modality in course.modality.all():
            return Response({'message': 'Modality already assigned'}, status=status.HTTP_400_BAD_REQUEST)
        course.modality.add(modality)
        return Response({'message': 'Modality assigned'}, status=status.HTTP_201_CREATED)


class TypeOfProgramAssignmentSerializer(APIView):
    permission_classes = [IsAdminUser]  # Permisos

    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        type_of_program_id = kwargs.get('type_of_program_id')
        course = get_object_or_404(Course, id=course_id)
        type_of_program = get_object_or_404(TypeOfProgram, id=type_of_program_id)
        if type_of_program in course.type_of_program.all():
            return Response({'message': 'Type of program already assigned'}, status=status.HTTP_400_BAD_REQUEST)
        course.type_of_program.add(type_of_program)
        type_of_program.number_of_courses += 1
        type_of_program.save()
        return Response({'message': 'Type of program assigned'}, status=status.HTTP_201_CREATED)

# Delete relationships

class CategoryDeleteAssignmentSerializer(APIView):
    permission_classes = [IsAdminUser]  # Permisos

    def delete(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        category_id = kwargs.get('category_id')
        course = get_object_or_404(Course, id=course_id)
        category = get_object_or_404(Category, id=category_id)
        if category not in course.category.all():
            return Response({'message': 'Category not assigned'}, status=status.HTTP_400_BAD_REQUEST)
        course.category.remove(category)
        category.number_of_courses -= 1
        category.save()
        return Response({'message': 'Category deleted'}, status=status.HTTP_200_OK)

class ModalityDeleteAssignmentSerializer(APIView):
    permission_classes = [IsAdminUser]  # Permisos

    def delete(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        modality_id = kwargs.get('modality_id')
        course = get_object_or_404(Course, id=course_id)
        modality = get_object_or_404(Modality, id=modality_id)
        if modality not in course.modality.all():
            return Response({'message': 'Modality not assigned'}, status=status.HTTP_400_BAD_REQUEST)
        course.modality.remove(modality)
        return Response({'message': 'Modality deleted'}, status=status.HTTP_200_OK)

class TypeOfProgramDeleteAssignmentSerializer(APIView):
    permission_classes = [IsAdminUser]  # Permisos

    def delete(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        type_of_program_id = kwargs.get('type_of_program_id')
        course = get_object_or_404(Course, id=course_id)
        type_of_program = get_object_or_404(TypeOfProgram, id=type_of_program_id)
        if type_of_program not in course.type_of_program.all():
            return Response({'message': 'Type of program not assigned'}, status=status.HTTP_400_BAD_REQUEST)
        course.type_of_program.remove(type_of_program)
        type_of_program.number_of_courses -= 1
        type_of_program.save()
        return Response({'message': 'Type of program deleted'}, status=status.HTTP_200_OK)


#filters

class CourseFilterView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    
    def get_queryset(self):
        queryset = Course.objects.all()
        university = self.request.query_params.getlist('university', [])
        category = self.request.query_params.getlist('category', [])
        modality = self.request.query_params.getlist('modality', [])
        type_of_program = self.request.query_params.getlist('typeofprogram', [])
        if university:
            queryset = reduce(lambda qs, p: qs & qs.filter(university=p), university, queryset)
        if category:
            queryset = reduce(lambda qs, p: qs & qs.filter(category=p), category, queryset)
        if modality:
            queryset = reduce(lambda qs, p: qs & qs.filter(modality=p), modality, queryset)
        if type_of_program:
            queryset = reduce(lambda qs, p: qs & qs.filter(type_of_program=p), type_of_program, queryset)

        return queryset.distinct()
