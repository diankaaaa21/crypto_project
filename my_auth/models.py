from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManage(BaseUserManager):
    def create_user(self, phone_number, first_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The phone number is required")
        user = self.model(
            phone_number=phone_number, first_name=first_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number, first_name, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(unique=True)
    first_name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "password"]

    objects = CustomUserManage()

    def __str__(self):
        return self.phone_number
