from rest_framework import (
    generics,
    permissions,
)
from functools import reduce
from django.shortcuts import get_object_or_404
from westudy.models import Course, University, Modality, Category, TypeOfProgram
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status, serializers
import datetime
from westudy.permissions import RegisterWithoutAuthPermission, IsAdminUser, IsUniversityAdmin
from rest_framework.pagination import PageNumberPagination
from django.db.models import F, ExpressionWrapper, fields
import boto3
from app import settings
from .serializers import (
    CourseSerializer,
    CourseCreateSerializer
)


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 8

    def get_page_size(self, request):
        return self.page_size


class CourseCreateView(generics.CreateAPIView):
    permission_classes = [IsUniversityAdmin]  # Permisos
    serializer_class = CourseCreateSerializer

    def perform_create(self, serializer):
        university_id = self.kwargs.get('id')
        try:
            university = University.objects.get(id=university_id)
            university.number_of_courses = university.number_of_courses + 1
            university.save()
            serializer.save(university=university,institution=university.name)
            return Response({'message': 'Course created'}, status=status.HTTP_201_CREATED)
        except University.DoesNotExist:
            raise serializers.ValidationError('University not found')

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # response con el id del curso creado
        response.data = {'message': 'Course created', 'id': response.data['id']}
        return response

class CourseListByUniversityView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission] # Permisos
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination
    pagination_class.page_size = 8

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
        course = get_object_or_404(Course, id=course_id)
        return course

class CourseUpdateView(generics.UpdateAPIView):
    """ Update a course """
    permission_classes = [IsUniversityAdmin]  # Permisos
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, University):
            return Course.objects.filter(university=user)
        else:
            return Course.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        course_id = self.kwargs.get('id')
        course = generics.get_object_or_404(queryset, id=course_id)
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
    permission_classes = [IsUniversityAdmin]  # Permisos
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, University):
            return Course.objects.filter(university=user)
        else:
            return Course.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        course_id = self.kwargs.get('id')
        course = generics.get_object_or_404(queryset, id=course_id)
        return course

    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        # eliminar number_of_courses de la universidad
        university = course.university
        university.number_of_courses = university.number_of_courses - 1
        university.save()
        if course.background_image:
            session = boto3.Session(
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
            s3 = session.resource('s3')
            bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
            bucket.Object(course.background_image.name).delete()
        course.delete()
        return Response({'message': 'Course deleted'}, status=status.HTTP_200_OK)

class CategoryAssignmentSerializer(APIView):
    permission_classes = [IsUniversityAdmin]  # Permisos

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, University):
            return Course.objects.filter(university=user)
        else:
            return Course.objects.all()
    
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        course_id = kwargs.get('course_id')
        category_id = kwargs.get('category_id')
        course = get_object_or_404(queryset, id=course_id)
        category = get_object_or_404(Category, id=category_id)
        if category in course.category.all():
            return Response({'message': 'Category already assigned'}, status=status.HTTP_400_BAD_REQUEST)
        course.category.add(category)
        category.number_of_courses += 1
        category.save()
        return Response({'message': 'Category assigned'}, status=status.HTTP_201_CREATED)

class ModalityAssignmentSerializer(APIView):
    permission_classes = [IsUniversityAdmin]  # Permisos

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, University):
            return Course.objects.filter(university=user)
        else:
            return Course.objects.all()

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        course_id = kwargs.get('course_id')
        modality_id = kwargs.get('modality_id')
        course = get_object_or_404(queryset, id=course_id)
        modality = get_object_or_404(Modality, id=modality_id)
        if modality in course.modality.all():
            return Response({'message': 'Modality already assigned'}, status=status.HTTP_400_BAD_REQUEST)
        course.modality.add(modality)
        return Response({'message': 'Modality assigned'}, status=status.HTTP_201_CREATED)


class TypeOfProgramAssignmentSerializer(APIView):
    permission_classes = [IsUniversityAdmin]  # Permisos

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, University):
            return Course.objects.filter(university=user)
        else:
            Course.objects.all()

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        course_id = kwargs.get('course_id')
        type_of_program_id = kwargs.get('type_of_program_id')
        course = get_object_or_404(queryset, id=course_id)
        type_of_program = get_object_or_404(TypeOfProgram, id=type_of_program_id)
        if type_of_program in course.type_of_program.all():
            return Response({'message': 'Type of program already assigned'}, status=status.HTTP_400_BAD_REQUEST)
        course.type_of_program.add(type_of_program)
        type_of_program.number_of_courses += 1
        type_of_program.save()
        return Response({'message': 'Type of program assigned'}, status=status.HTTP_201_CREATED)

class CategoryDeleteAssignmentSerializer(APIView):
    permission_classes = [IsUniversityAdmin]  # Permisos

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, University):
            return Course.objects.filter(university=user)
        else:
            Course.objects.all()

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        course_id = kwargs.get('course_id')
        category_id = kwargs.get('category_id')
        course = get_object_or_404(queryset, id=course_id)
        category = get_object_or_404(Category, id=category_id)
        if category not in course.category.all():
            return Response({'message': 'Category not assigned'}, status=status.HTTP_400_BAD_REQUEST)
        course.category.remove(category)
        category.number_of_courses -= 1
        category.save()
        return Response({'message': 'Category deleted'}, status=status.HTTP_200_OK)

class ModalityDeleteAssignmentSerializer(APIView):
    permission_classes = [IsUniversityAdmin]  # Permisos

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, University):
            return Course.objects.filter(university=user)
        else:
            Course.objects.all()

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        course_id = kwargs.get('course_id')
        modality_id = kwargs.get('modality_id')
        course = get_object_or_404(queryset, id=course_id)
        modality = get_object_or_404(Modality, id=modality_id)
        if modality not in course.modality.all():
            return Response({'message': 'Modality not assigned'}, status=status.HTTP_400_BAD_REQUEST)
        course.modality.remove(modality)
        return Response({'message': 'Modality deleted'}, status=status.HTTP_200_OK)

class TypeOfProgramDeleteAssignmentSerializer(APIView):
    permission_classes = [IsUniversityAdmin]  # Permisos

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, University):
            return Course.objects.filter(university=user)
        else:
            Course.objects.all()

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        course_id = kwargs.get('course_id')
        type_of_program_id = kwargs.get('type_of_program_id')
        course = get_object_or_404(queryset, id=course_id)
        type_of_program = get_object_or_404(TypeOfProgram, id=type_of_program_id)
        if type_of_program not in course.type_of_program.all():
            return Response({'message': 'Type of program not assigned'}, status=status.HTTP_400_BAD_REQUEST)
        course.type_of_program.remove(type_of_program)
        type_of_program.number_of_courses -= 1
        type_of_program.save()
        return Response({'message': 'Type of program deleted'}, status=status.HTTP_200_OK)

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
        shift = self.request.query_params.getlist('shift', [])
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        min_duration = self.request.query_params.get('min_duration', None)
        max_duration = self.request.query_params.get('max_duration', None)

        if university:
            queryset = reduce(lambda qs, p: qs & qs.filter(university=p), university, queryset)
        if category:
            queryset = reduce(lambda qs, p: qs & qs.filter(category=p), category, queryset)
        if modality:
            queryset = reduce(lambda qs, p: qs & qs.filter(modality=p), modality, queryset)
        if type_of_program:
            queryset = reduce(lambda qs, p: qs & qs.filter(type_of_program=p), type_of_program, queryset)
        if shift:
            #shift = ['Tarde', 'Noche']
            q_objects = Q()  # Objeto Q inicial vacío
            # Iterar sobre la lista de palabras y agregar Q objects con operador OR
            for x in shift:
                q_objects &= Q(shifts__shift__icontains=x)
            #queryset = queryset.filter(shifts__shift__icontains__in=shift)
            queryset = queryset.filter(q_objects)

        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)
    
        if min_duration is not None:
            min_duration = int(min_duration)
        if max_duration is not None:
            max_duration = int(max_duration)

        duration_expression = ExpressionWrapper(F('end_of_course') - F('start_of_course'), output_field=fields.DurationField())
        if min_duration is not None:
            queryset = queryset.annotate(duration=duration_expression).filter(duration__gte=datetime.timedelta(days=min_duration))
        if max_duration is not None:
            queryset = queryset.annotate(duration=duration_expression).filter(duration__lte=datetime.timedelta(days=max_duration))

        return queryset.distinct()
