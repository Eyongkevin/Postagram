from rest_framework.permissions import SAFE_METHODS, BasePermission


class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        # if view.basename in ["post"]:
        if not bool(request.user and request.user.is_authenticated):
            return False
        # if request.method in ["DELETE", "PUT", "PATCH"]:
        #     return request.user == obj.author
        return True

    def has_permission(self, request, view):
        # if view.basename in ["post", "post-comment"]:
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        return bool(request.user and request.user.is_authenticated)
