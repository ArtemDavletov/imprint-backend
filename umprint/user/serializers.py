from rest_framework import serializers
from user.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ("id", "password")
