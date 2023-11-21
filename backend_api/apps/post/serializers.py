from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.abstract import AbstractSerializer
from apps.user.serializers import UserSerializer

from .models import Post


# ? During posting of post, the author shouldn't be required for user to input.
# ? We should get it from the authenticated user.
class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), slug_field="public_id"
    )

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't create or update a post for another user.")
        return value

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = get_user_model().objects.get_object_by_public_id(rep.get("author"))
        rep["author"] = UserSerializer(author).data
        return rep

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data["edited"] = True
        return super().update(instance, validated_data)

    class Meta:
        model = Post
        fields = ("id", "author", "body", "edited", "created", "updated")
        read_only_fields = ("edited",)
