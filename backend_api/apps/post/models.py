from django.db import models

from apps.core.abstract import AbstractManager, AbstractModel

# Create your models here.


class PostManager(AbstractManager):
    pass


class Post(AbstractModel):
    author = models.ForeignKey(
        to="apps_user.User", on_delete=models.CASCADE, related_name="post"
    )
    body = models.TextField()
    edited = models.BooleanField(default=False)

    objects = PostManager()

    def __str__(self) -> str:
        return f"{self.author.name}"
