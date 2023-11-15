from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.user import models
from apps.user.serializers import UserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ("patch", "get")
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.User.objects.all()
        return models.User.objects.exclude(is_superuser=True)

    def get_object(self):
        obj = models.User.objects.get_object_by_public_id(self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj
