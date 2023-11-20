from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.abstract import AbstractSerializer
from apps.user.serializers import UserSerializer

from .models import Post


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), slug_field="public_id"
    )

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't create a post for another user.")
        return value

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = get_user_model().objects.get_object_by_public_id(rep.get("author"))
        rep["author"] = UserSerializer(author).data
        return rep

    class Meta:
        model = Post
        fields = ("id", "author", "body", "edited", "created", "updated")
        read_only_fields = ("edited",)
