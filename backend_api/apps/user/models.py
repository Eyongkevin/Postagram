from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from apps.core.abstract import AbstractManager, AbstractModel


# Create your models here.
class UserManager(BaseUserManager, AbstractManager):
    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""

        if username is None:
            raise TypeError("User must have a username")
        if email is None:
            raise TypeError("User must have an email")
        if password is None:
            raise TypeError("User must have a password")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        """Create and return '`User` with superuser (admin) permissions"""

        if username is None:
            raise TypeError("Superuser must have a username")
        if email is None:
            raise TypeError("Superuser must have an email")
        if password is None:
            raise TypeError("Superuser must have a password")

        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, AbstractModel):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    posts_liked = models.ManyToManyField("apps_post.Post", related_name="liked_by")
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def like(self, post):
        return self.posts_liked.add(post)

    def remove_like(self, post):
        return self.posts_liked.remove(post)

    def has_liked(self, post):
        return self.posts_liked.filter(pk=post.pk).exists()

    def __str__(self) -> str:
        return f"{self.email}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
