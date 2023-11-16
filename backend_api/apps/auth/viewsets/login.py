from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from apps.auth.serializers import LoginSerializer


class LoginViewSet(ViewSet):
    http_method_names = ("post",)
    serializer_classes = LoginSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_classes(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e
        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )
