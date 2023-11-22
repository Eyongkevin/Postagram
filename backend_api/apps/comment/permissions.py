from rest_framework.permissions import SAFE_METHODS, BasePermission


class CommentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        anonymous users can only perform safe operations

        superuser can delete  all comments

        author of a post can delete all comments of that post

        author of a comment can update and delete the comment.
        """
        if view.basename in ["post-comment"]:
            if request.method in ["DELETE"]:
                if request.user.is_superuser:
                    return True
                if obj.post is not None:
                    return obj.post.author == obj.author

                obj_post = obj.post
                obj_copy = obj
                while obj_post is None:
                    replied_to = obj_copy.replied_to
                    if replied_to.post is not None:
                        return replied_to.post.author == request.user
                    obj_post = replied_to.post
                    obj_copy = replied_to

            if request.method in ["PUT", "PATCH"]:
                return request.user == obj.author

        return True
