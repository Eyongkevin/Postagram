from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r"v1/user", views.UserViewSet, basename="user")

urlpatterns = [
    *router.urls,
]
