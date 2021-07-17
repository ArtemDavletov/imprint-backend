from browser.models import InstanceBrowser
from rest_framework import serializers


class CreateBrowserInstanceSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, required=True)
    description = serializers.CharField(max_length=500, required=False)

    browser_type = serializers.CharField(max_length=10, required=True)
    browser_engine = serializers.CharField(max_length=10, required=True)

    folder_id = serializers.UUIDField(required=False)

    class Meta:
        model = InstanceBrowser

    def create(self, *args, **kwargs) -> InstanceBrowser:
        return InstanceBrowser.objects.create(**self.validated_data)

    def update(self, instance, validated_data) -> InstanceBrowser:
        return instance.objects.update(**validated_data)


class BrowserInstanceSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(max_length=20)
    description = serializers.CharField(max_length=500)

    type = serializers.ReadOnlyField()
    engine = serializers.ReadOnlyField()

    # Folder fields
    folder_uuid = serializers.ReadOnlyField()
    folder_name = serializers.ReadOnlyField()
    folder_description = serializers.ReadOnlyField()

    class Meta:
        model = InstanceBrowser


class UpdateBrowserInstanceSerializer(CreateBrowserInstanceSerializer):
    name = serializers.CharField(max_length=20, required=False)

    browser_type = serializers.CharField(required=False)
    browser_engine = serializers.CharField(required=False)

    folder_id = serializers.UUIDField(required=False)
