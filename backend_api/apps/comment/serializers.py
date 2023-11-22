from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.comment.models import Comment
from apps.core.abstract import AbstractSerializer
from apps.post.models import Post
from apps.user.serializers import UserSerializer


class CommentSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), slug_field="public_id"
    )
    post = serializers.SlugRelatedField(
        queryset=Post.objects.all(),
        slug_field="public_id",
        required=False,
        # read_only=True,
    )
    replied_to = serializers.SlugRelatedField(
        queryset=Comment.objects.all(),
        slug_field="public_id",
        required=False,
        # Can't have this field if you are providing queryset above
        # read_only=True,
    )
    replies = serializers.SerializerMethodField(read_only=True)

    def get_replies(self, instance):
        replies = instance.comment_replied.all()
        return CommentSerializer(replies, many=True).data

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError("You can't create comment for another user")
        return value

    def validate_post(self, value):
        # If it's not a delete, put or patch, then self.instance is set to None
        if self.instance:
            return self.instance.post
        return value

    def validate_replied_to(self, value):
        if self.instance:
            return self.instance.replied_to
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
        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "body",
            "replied_to",
            "replies",
            "edited",
            "created",
            "updated",
        )
        read_only_fields = ("edited",)
        # doesn't work for fields that are explicitly defined in the serializer like 'replied_to', 'post' and 'replies'
        # read_only_fields = ("edited", "replied_to", "post", "replies")
