from rest_framework import routers

from .views import PostViewSet

router = routers.SimpleRouter()

router.register(r"v1/post", PostViewSet, basename="post")

urlpatterns = [
    *router.urls,
]
