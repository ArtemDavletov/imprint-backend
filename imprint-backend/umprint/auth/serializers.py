from django.db.models import Q
from django.http import QueryDict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "login",
            "email",
            "password",
            "first_name",
            "second_name",
            "telegram_login",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }


class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):

        request = self.context["request"]

        request_data: QueryDict = request.data
        username: str = request_data.get("login")
        password: str = request_data.get("password")

        try:
            user = UserProfile.objects.get(Q(login=username) | Q(email=username))
        except:
            return super().validate(attrs=attrs)

        if user.password == password:
            refresh: RefreshToken = super().get_token(user)

            return dict(refresh=str(refresh), access=str(refresh.access_token))

        return super().validate(attrs=attrs)
