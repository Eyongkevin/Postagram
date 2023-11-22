from django.core.exceptions import ValidationError
from django.db import models

from apps.core.abstract import AbstractManager, AbstractModel


# Create your models here.
class CommentManager(AbstractManager):
    pass


class Comment(AbstractModel):
    post = models.ForeignKey(
        "apps_post.Post",
        related_name="comment_post",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        "apps_user.User", related_name="comment_author", on_delete=models.CASCADE
    )
    replied_to = models.ForeignKey(
        "self",
        related_name="comment_replied",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    body = models.TextField()
    edited = models.BooleanField(default=False)

    objects = CommentManager()

    class Meta:
        #! DB level check. This is application when the object's 'create' or model's save method is called.
        constraints = [
            # Make sure, post or replied_to is None, but not both
            models.CheckConstraint(
                check=(models.Q(post__isnull=True) | models.Q(replied_to__isnull=True))
                & ~(models.Q(post__isnull=True) & models.Q(replied_to__isnull=True)),
                name="check_post_and_replied_to",
            )
        ]

    #! Model level check. This is application when the model's full_clean method is called.
    def clean(self) -> None:
        """Make sure, post or replied_to is None, but not both"""

        if (self.post and self.replied_to) or (
            self.post is not None and self.replied_to is not None
        ):
            raise ValidationError(
                "The fields 'replied_to' and 'post' shouldn't be provided at the same time."
            )

    def __str__(self):
        return f"{self.author.name} -> {self.body[:30]}..."
