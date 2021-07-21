from uuid import UUID

from browser.models import (
    BrowserEngine,
    BrowserType,
    InstanceBrowser,
    UserProfileInstanceBrowserRelation,
)
from browser.serializers import (
    BrowserInstanceSerializer,
    CreateBrowserInstanceSerializer,
    UpdateBrowserInstanceSerializer,
    BrowserInstanceConfigSerializer,
)
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from browser.config_models import ConfigModel


class CreateBrowserInstance(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    create_serializer = CreateBrowserInstanceSerializer
    serializer_class = BrowserInstanceSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """
        Создает новый browser
        """
        serializer = self.create_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance_browser: InstanceBrowser = serializer.save()

        UserProfileInstanceBrowserRelation.objects.create(
            browser=instance_browser,
            user=request.user,
            rule_type=UserProfileInstanceBrowserRelation.RulesChoices.ADMIN.value,
            is_creator=True,
        )

        return Response(data=self.serializer_class(instance_browser).data)


class UpdateBrowserInstance(generics.UpdateAPIView):
    ADDICTION_FIELDS = {"browser_type": BrowserType, "browser_engine": BrowserEngine}

    permission_classes = (IsAuthenticated,)
    update_serializer = UpdateBrowserInstanceSerializer
    serializer_class = BrowserInstanceSerializer

    def pull_addiction_id(self, data):
        """
        Attention! Every config have to have field "name"

        Function changes every config name to config_id
        """
        for field in self.ADDICTION_FIELDS:
            if field in data:
                try:
                    data[field] = (
                        self.ADDICTION_FIELDS[field].objects.get(name=data[field]).id
                    )
                except self.ADDICTION_FIELDS[field].DoesNotExist:
                    del data[field]
                except Exception:
                    del data[field]

        return data

    def post(self, request, browser_uuid: UUID, *args, **kwargs) -> Response:
        """
        Возвращает информацию о browser оп его uuid
        """

        serializer = self.update_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        update_data = serializer.validated_data

        try:
            relation = UserProfileInstanceBrowserRelation.objects.get(
                browser_id=browser_uuid, user_id=request.user.id
            )
        except UserProfileInstanceBrowserRelation.DoesNotExist:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        if relation.rule_type in UserProfileInstanceBrowserRelation.ACCESS_TO_EDIT:
            update_data = self.pull_addiction_id(update_data)

            InstanceBrowser.objects.filter(id=relation.browser_id).update(**update_data)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class GetBrowserInstance(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BrowserInstanceSerializer

    def get(self, request, browser_uuid: UUID) -> Response:
        """
        Возвращает информацию о browser оп его uuid
        """

        response = {}

        try:
            instance_browser = self.serializer_class(
                InstanceBrowser.objects.get(id=browser_uuid)
            )

            response["data"] = instance_browser.data
        except InstanceBrowser.DoesNotExist:
            response["status"] = status.HTTP_404_NOT_FOUND

        return Response(**response)


class GetAllBrowserInstance(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BrowserInstanceSerializer

    def get(self, request) -> Response:
        """
        Возвращает все browser доступные пользователю
        """

        response = {}

        try:
            all_relations = UserProfileInstanceBrowserRelation.objects.filter(
                user_id=request.user.id
            ).select_related()

            response["data"] = list(
                map(
                    lambda relation: self.serializer_class(relation.browser).data,
                    all_relations,
                )
            )
        except InstanceBrowser.DoesNotExist:
            response["status"] = status.HTTP_404_NOT_FOUND

        return Response(**response)


class GetBrowserInstanceConfig(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BrowserInstanceConfigSerializer

    def get(self, request, browser_uuid: UUID) -> Response:
        """
        Возвращает информацию о browser оп его uuid
        """

        response = {}

        try:
            instance_browser = InstanceBrowser.objects.get(id=browser_uuid)
            config = ConfigModel.objects.get(id=instance_browser.config_id)

            response["data"] = instance_browser.data
        except InstanceBrowser.DoesNotExist:
            response["status"] = status.HTTP_404_NOT_FOUND

        return Response(**response)


@api_view(["PUT"])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def move_browser_instance(request, browser_uuid: UUID, folder_uuid: UUID):
    """
    /browser/move/<browser_uuid>/<folder_uuid>

    Перемещает или добавляет browser в folder по folder_uuid
    """
    response = {}

    try:
        InstanceBrowser.objects.filter(id=browser_uuid).update(folder_id=folder_uuid)
        response["data"] = {"message", "Browser is successfully moved"}
        response["status"] = status.HTTP_200_OK
    except Exception:
        response["status"] = status.HTTP_400_BAD_REQUEST

    return Response(**response)
