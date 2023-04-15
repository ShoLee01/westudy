from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from westudy.models import University
from rest_framework import exceptions

class CombinedJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Primero intenta autenticar como University´
        print('CombinedJWTAuthentication')
        print(request)
        university_auth = UniversityJWTAuthentication()
        auth_result = university_auth.authenticate(request)

        if auth_result != (None, None):
            # Si tiene éxito, devuelve el resultado de la autenticación de la universidad
            return auth_result
        else:
            # Si no, intenta autenticar como usuario normal
            return super().authenticate(request)


class UniversityJWTAuthentication(JWTAuthentication):
        
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None, None

        validated_token = self.get_validated_token(self.get_raw_token(header))

        if 'university_id' not in validated_token:
            return None, None

        return self.get_user(validated_token), validated_token

    def get_user(self, validated_token):
        university_id = validated_token['university_id']
        try:
            university = University.objects.get(id=university_id)
        except University.DoesNotExist:
            return None

        return university




