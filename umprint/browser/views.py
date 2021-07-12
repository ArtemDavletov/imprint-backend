from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.response import Response

from browser.serializers import CreateBrowserInstanceSerializer, AddBrowserSerializer

from browser.models import InstanceBrowser

from browser.models import BrowserType, BrowserEngine, Folder


class AddBrowserInstance(generics.GenericAPIView):
    serializer_class = AddBrowserSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_browser_type: BrowserType = BrowserType.objects.create(**serializer.validated_data)

        return Response(data=model_to_dict(new_browser_type))


class CreateBrowserInstance(generics.GenericAPIView):
    serializer_class = CreateBrowserInstanceSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=model_to_dict(serializer.create()))
