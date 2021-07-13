from auth.serializers import AuthTokenObtainPairSerializer
from auth.serializers import RegisterSerializer, UserSerializer
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token",
        })


class AuthTokenObtainPairView(TokenObtainPairView):
    serializer_class = AuthTokenObtainPairSerializer
    parser_classes = [JSONParser]
