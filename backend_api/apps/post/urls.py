# from rest_framework import routers
from rest_framework_nested import routers

from apps.comment.views import CommentViewSet

from .views import PostViewSet

router = routers.SimpleRouter()

router.register(r"v1/post", PostViewSet, basename="post")
posts_router = routers.NestedSimpleRouter(router, r"v1/post", lookup="post")
posts_router.register(r"comment", CommentViewSet, basename="post-comment")

urlpatterns = [
    *router.urls,
    *posts_router.urls,
]
