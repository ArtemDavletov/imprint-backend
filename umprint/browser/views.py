from uuid import UUID

from browser.models import InstanceBrowser
from browser.models import UserProfile, UserProfileInstanceBrowserRelation
from browser.serializers import CreateBrowserInstanceSerializer, UpdateBrowserInstanceSerializer, \
    BrowserInstanceSerializer
from django.forms import model_to_dict
from rest_framework import generics, status
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from browser.models import Folder


class CreateBrowserInstance(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    create_serializer = CreateBrowserInstanceSerializer
    serializer_class = BrowserInstanceSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.create_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance_browser: InstanceBrowser = serializer.create()

        UserProfileInstanceBrowserRelation.objects.create(
            browser=instance_browser,
            user=request.user,
            rule_type=UserProfileInstanceBrowserRelation.RulesChoices.ADMIN.value,
            is_creator=True
        )

        return Response(data=self.serializer_class(instance_browser).data)


class UpdateBrowserInstance(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    update_serializer = UpdateBrowserInstanceSerializer
    serializer_class = BrowserInstanceSerializer

    def post(self, request, browser_uuid: UUID, *args, **kwargs):
        serializer = self.update_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_data = serializer.validated_data

        if "folder_name" in request.data:
            folder, created = Folder.objects.get_or_create(name=request.data["folder_name"])
            update_data["folder_name"] = folder.id

        relation = UserProfileInstanceBrowserRelation.objects.get(
            browser_id=browser_uuid, user_id=request.user.id
        )

        if relation.rule_type in UserProfileInstanceBrowserRelation.ACCESS_TO_EDIT:
            InstanceBrowser.objects \
                .filter(id=relation.browser_id) \
                .update(**update_data)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class GetBrowserInstance(generics.GenericAPIView):
    serializer_class = BrowserInstanceSerializer

    def get(self, request, browser_uuid: UUID) -> Response:
        response = {}

        try:
            instance_browser = self.serializer_class(InstanceBrowser.objects.get(id=browser_uuid))

            response["data"] = instance_browser.data
        except:
            response["status"] = status.HTTP_404_NOT_FOUND

        return Response(**response)
