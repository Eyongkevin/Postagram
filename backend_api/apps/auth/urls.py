from rest_framework import routers

from . import viewsets

router = routers.SimpleRouter()

router.register(r"v1/auth/register", viewsets.RegisterViewSet, basename="auth-register")
router.register(r"v1/auth/login", viewsets.LoginViewSet, basename="auth-login")
router.register(r"v1/auth/refresh", viewsets.RefreshViewSet, basename="auth-refresh")

urlpatterns = [
    *router.urls,
]
