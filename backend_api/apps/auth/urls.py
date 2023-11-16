from rest_framework import routers

from . import viewsets

router = routers.SimpleRouter()

router.register(r"auth/register", viewsets.RegisterViewSet, basename="auth-register")
router.register(r"auth/login", viewsets.LoginViewSet, basename="auth-login")

urlpatterns = [
    *router.urls,
]
