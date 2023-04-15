from django.contrib.auth.backends import BaseBackend
from westudy.models import University, User

class UniversityAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        model = kwargs.get('model')
        if model == User:
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        elif model == University:
            try:
                university = University.objects.get(email=email)
                if university.check_password(password):
                    return university
            except University.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            try:
                return University.objects.get(pk=user_id)
            except University.DoesNotExist:
                return None