from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r"user", views.UserViewSet, basename="user")

urlpatterns = [
    *router.urls,
]
