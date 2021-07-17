from uuid import UUID

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from user.models import UserProfile
from user.serializers import UserSerializer


class UserProfileView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request: Request, user_id: UUID) -> Response:
        try:
            return Response(
                data=UserSerializer(UserProfile.objects.get(id=user_id)).data
            )
        except UserProfile.DoesNotExist:
            return Response(
                data={"message": "No such user"}, status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request: Request, user_id: UUID) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserProfile.objects.filter(id=user_id).update(**serializer.validated_data)

        return Response(data={"status": "success"})
