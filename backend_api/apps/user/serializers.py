from rest_framework import serializers

from apps.user import models


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="public_id", read_only=True, format="hex")

    class Meta:
        model = models.User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "bio",
            "avatar",
            "is_active",
            "created",
            "updated",
        )
        read_only_field = ("is_active", "created", "updated")
