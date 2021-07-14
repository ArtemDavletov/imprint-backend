from browser.models import BrowserType, BrowserEngine, Folder
from browser.models import InstanceBrowser
from rest_framework import serializers


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

    def update(self, instance, validated_data) -> InstanceBrowser:
        return instance.objects.update(**validated_data)


class BrowserInstanceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=500)

    type = serializers.ReadOnlyField()
    engine = serializers.ReadOnlyField()
    foldername = serializers.ReadOnlyField()

    class Meta:
        model = InstanceBrowser


class UpdateBrowserInstanceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, required=False)
    description = serializers.CharField(max_length=500, required=False)

    type = serializers.ReadOnlyField(required=False)
    engine = serializers.ReadOnlyField(required=False)
    foldername = serializers.ReadOnlyField(required=False)

    class Meta:
        model = InstanceBrowser
