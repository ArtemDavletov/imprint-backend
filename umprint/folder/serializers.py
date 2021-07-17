from browser.models import Folder
from rest_framework import serializers


class FolderSerializer(serializers.Serializer):
    folder_uuid = serializers.ReadOnlyField(required=False)
    name = serializers.CharField(max_length=20, required=True)
    description = serializers.CharField(max_length=500, required=True)

    class Meta:
        model = Folder
        fields = ("folder_uuid", "name", "description")


class ShareFolderSerializer(serializers.Serializer):
    RULES_CHOICES = (
        ("VIEW", "VIEW"),
        ("EDIT", "EDIT"),
        ("ADMIN", "ADMIN"),
    )

    rule = serializers.ChoiceField(choices=RULES_CHOICES)
