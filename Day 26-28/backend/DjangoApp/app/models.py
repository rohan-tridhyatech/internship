# myapp/models.py
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils.timezone import now, timedelta
import random



class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    contact = models.CharField(max_length=15, unique=False)
    is_active = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiration = models.DateTimeField(blank=True, null=True)

    # Use the custom manager
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'contact']

    def save(self, *args, **kwargs):
        # Check if the password needs hashing
        if not self.password.startswith(("pbkdf2_", "argon2$", "bcrypt$")):
            self.set_password(self.password) 

        super().save(*args, **kwargs)
        
    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.otp_expiration = now() + timedelta(minutes=10)  # OTP valid for 10 minutes
        self.save()    