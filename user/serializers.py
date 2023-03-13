from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _ # This is used to translate the error messages
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"

    def list(self, request):
        queryset = get_user_model().objects.all()
        serializer = UserListSerializer(queryset, many=True)
        return Response(serializer.data)
    

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["id","email", "password", "names", "surnames", "nationality", "date_of_birth",]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
    
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(TokenObtainPairSerializer):
    pass
