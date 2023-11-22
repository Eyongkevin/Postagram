from django.http.response import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from apps.auth.permissions import UserPermission
from apps.core.abstract import AbstractViewSet

from .models import Comment
from .permissions import CommentPermission
from .serializers import CommentSerializer

# Create your views here.


class CommentViewSet(AbstractViewSet):
    http_method_names = ("post", "get", "put", "delete")
    permission_classes = (UserPermission, CommentPermission)
    serializer_class = CommentSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Comment.objects.all()
        post_pk = self.kwargs["post_pk"]
        if post_pk is None:
            return Http404

        queryset = Comment.objects.filter(post__public_id=post_pk)

        return queryset

    def get_object(self):
        obj = Comment.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
