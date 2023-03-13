from rest_framework import (
    generics,
    permissions,
)
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from westudy.models import Course, TypeOfProgram
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from westudy.permissions import RegisterWithoutAuthPermission, IsAdminUser

from user.serializers import (
    UserSerializer,
    UserListSerializer,
    AuthTokenSerializer,
)

from course.serializers import (
    CourseSerializer,
)

class CreateUserView(generics.CreateAPIView):  # Creando vista de usuario
    authentication_classes = []
    permission_classes = [RegisterWithoutAuthPermission]  # Permisos
    serializer_class = UserSerializer

class ProgramPreferenceView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Permisos

    def post(self, request, *args, **kwargs):
        program_id = self.kwargs.get('id')
        try:
            program = TypeOfProgram.objects.get(id=program_id)
            user = self.request.user
            if program in user.program_preferences.all():
                raise serializers.ValidationError('Program already exists')
            user.program_preferences.add(program)
            return Response({'message': 'Program added to favorites'}, status=status.HTTP_201_CREATED)
        except TypeOfProgram.DoesNotExist:
            raise serializers.ValidationError('Program not found')


class CreateFavoriteCourseView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Permisos

    def post(self, request, *args, **kwargs):
        course_id = self.kwargs.get('id')
        try:
            course = Course.objects.get(id=course_id)
            user = self.request.user
            if course in user.saved_courses.all():
                raise serializers.ValidationError('Course already in favorites')
            user.saved_courses.add(course)
            user.save()
            return Response({'message': 'Course added to favorites'}, status=status.HTTP_201_CREATED)
        except Course.DoesNotExist:
            raise serializers.ValidationError('Course not found')

class ManageViewOfCoursesAssociatedUser(generics.ListAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]  # Permisos

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(saved_courses=user)

class DeleteFavoriteCourseView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CourseSerializer

    def delete(self, request, *args, **kwargs):
        course_id = self.kwargs.get('id')
        print(self.kwargs)
        try:
            course = Course.objects.get(id=course_id)
            user = self.request.user
            if course not in user.saved_courses.all():
                return Response({'error': 'Course not found in favorites'}, status=status.HTTP_404_NOT_FOUND)
            user.saved_courses.remove(course)
            user.save()
            return Response({'message': 'Course removed from favorites'}, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

class Login(TokenObtainPairView):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data['access'],
                    'refresh': login_serializer.validated_data['refresh'], 
                    'user': user_serializer.data,
                    'message': 'Login successful'},status=status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ManageUserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]  # Permisos

    def get_queryset(self):
        return get_user_model().objects.all()

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer  # Serializador de usuario
    permission_classes = [permissions.IsAuthenticated]  # Permisos

    def get_object(self):
        return self.request.user

class ManageDeleteView(generics.DestroyAPIView):
    serializer_class = UserSerializer  # Serializador de usuario
    permission_classes = [permissions.IsAuthenticated]  # Permisos

    def get_object(self):
        return self.request.user
