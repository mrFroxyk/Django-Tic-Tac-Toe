from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
class CustomUser(AbstractUser):
    is_quest = models.BooleanField(default=False)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']
#
#     def __str__(self):
#         return self.email
