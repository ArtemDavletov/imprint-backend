from uuid import UUID

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from user.models import UserProfile
from user.serializers import UserSerializer


@api_view(["POST"])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def user_view(self, request: Request, user_id: UUID) -> Response:
    """
    Возвращает информацию о пользователе
    Изменяет информацию о пользователе
    """
    if request.method == "GET":
        try:
            return Response(
                data=UserSerializer(UserProfile.objects.get(id=user_id)).data
            )
        except UserProfile.DoesNotExist:
            return Response(
                data={"message": "No such user"}, status=status.HTTP_404_NOT_FOUND
            )

    elif request.method == "PUT":
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        UserProfile.objects.filter(id=user_id).update(**serializer.validated_data)

        return Response(data={"status": "success"})
