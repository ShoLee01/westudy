from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.translation import gettext_lazy as _
from westudy.models import University

class UniversityAccessToken(AccessToken):
    access_token = None
    user_id_claim = 'university_id'  # Agregue esta línea
    username_claim = 'email'  # Agregue esta línea

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.token:
            self.access_token = self.token

    @classmethod
    def for_user(cls, user):
        token = cls()
        token[cls.user_id_claim] = user.pk

        if hasattr(user, 'email'):
            token[cls.username_claim] = user.email

        return token

    @property
    def user(self):
        try:
            user_id = self.token[self.user_id_claim]
        except KeyError:
            raise TokenError(self.user_id_claim, _('Token contained no recognizable user identification'))

        try:
            university = University.objects.get(id=user_id)
        except University.DoesNotExist:
            raise TokenError(self.user_id_claim, _('User not found'))

        if not university.is_active:
            raise TokenError(self.user_id_claim, _('User is inactive'))

        return university

