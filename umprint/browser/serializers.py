from browser.models import BrowserType, BrowserEngine, Folder
from browser.models import InstanceBrowser
from rest_framework import serializers


class AddBrowserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)


class CreateBrowserInstanceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)

    browser_type = serializers.CharField(max_length=10)
    browser_engine = serializers.CharField(max_length=10)

    folder_name = serializers.CharField(max_length=10)

    def validate(self, attrs):
        data = {
            "name": attrs.get("name"),
            "browser_type": BrowserType.objects.get(name=attrs.get("browser_type")),
            "browser_engine":
                BrowserEngine.objects.get(engine_type=attrs.get("browser_engine")),
            "folder_name": Folder.objects.get_or_create(name=attrs.get("folder_name"))[0],
        }
        return data

    def create(self, *args, **kwargs) -> InstanceBrowser:
        return InstanceBrowser.objects.create(**self.validated_data)

    def update(self, instance: InstanceBrowser, validated_data) -> InstanceBrowser:
        return instance.objects.update(**validated_data)
