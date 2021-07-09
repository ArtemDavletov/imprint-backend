import json

from django.http import QueryDict
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from user.models import UserProfile


class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):

        request = self.context["request"]

        request_data: QueryDict = request.data
        username: str = request_data.get("username")
        password: str = request_data.get("password")

        user = UserProfile.objects.get(login=username)

        if user is None:
            user = UserProfile.objects.get(email=username)

            if user is None:
                return super().validate(attrs=attrs)

        if user.password == password:
            refresh: RefreshToken = super().get_token(user)

            return dict(refresh=str(refresh), access=str(refresh.access_token))

        return super().validate(attrs=attrs)


class AuthTokenObtainPairView(TokenObtainPairView):
    serializer_class = AuthTokenObtainPairSerializer
