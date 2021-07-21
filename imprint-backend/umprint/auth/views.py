from auth.serializers import AuthTokenObtainPairSerializer, RegisterSerializer
from django.db import IntegrityError
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import UserSerializer


def extract_detail_from_integrity_error(error: IntegrityError):
    try:
        return error.args[0].split("\n")[1]
    except (AttributeError, IndexError):
        return error


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request, *args, **kwargs) -> Response:
        """
        Регистрирует пользователя
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            data={
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User Created Successfully. Now perform Login to get your token",
            }
        )


class AuthTokenObtainPairView(TokenObtainPairView):
    serializer_class = AuthTokenObtainPairSerializer

    def get_serializer_class(self):
        return self.serializer_class
