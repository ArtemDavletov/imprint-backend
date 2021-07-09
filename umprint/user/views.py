from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from django.forms.models import model_to_dict

from user.models import UserProfile


@api_view(['POST'])
def create_user(request: Request) -> Response:
    return Response(data=model_to_dict(UserProfile.objects.create(**request.data)))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request: Request, id: str) -> Response:
    return Response(data=model_to_dict(UserProfile.objects.get(_id=id)))


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request: Request) -> Response:
    UserProfile.objects.filter(login=request.data['login']).update(**request.data)
    return Response(data={"status": "success"})
