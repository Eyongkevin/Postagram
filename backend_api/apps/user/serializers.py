from apps.core.abstract import AbstractSerializer
from apps.user import models


class UserSerializer(AbstractSerializer):
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
        read_only_fields = ("is_active", "created", "updated")
