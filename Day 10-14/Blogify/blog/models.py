from __future__ import annotations

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("user", "User"),
        ("admin", "Admin"),
        ("author", "Author"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=False)

    def save(self, *args, **kwargs):
        # Set permissions based on the role
        if self.role == "admin":
            self.is_superuser = True
            self.is_staff = True
        elif self.role == "author":
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False

        # Check if the password needs hashing
        if not self.password.startswith(("pbkdf2_", "argon2$", "bcrypt$")):
            self.set_password(self.password)  # Hash the password

        # Call the parent class's save method
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
