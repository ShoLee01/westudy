from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from university.university_tokens import UniversityAccessToken
from westudy.models import University
from django.contrib.auth import (
    authenticate,
)
from university.serializers import (
    UniversitySerializer,
)

class UniversityTokenObtainPairSerializer(TokenObtainSerializer):
    def validate(self, attrs):
        university = authenticate(
            self.context['request'],
            email=attrs['email'],
            password=attrs['password'],
            model=University,
        )

        if university:
            if not university.is_active:
                raise serializers.ValidationError('Account not active')
            refresh = UniversityRefreshToken.for_university(university)
            access = UniversityAccessToken.for_user(university)
            university_serializer = UniversitySerializer(university)
            return {'university': university_serializer.data, 'access': str(access), 'refresh': str(refresh)}
        else:
            raise serializers.ValidationError('Invalid credentials')

class UniversityRefreshToken(RefreshToken):
    @classmethod
    def for_university(cls, university):
        token = cls()
        token.payload['university_id'] = university.id
        return token

    def bind_university(self, university):
        self.payload['university_id'] = university.id

    def get_university(self):
        university_id = self.payload['university_id']
        return University.objects.get(id=university_id)
