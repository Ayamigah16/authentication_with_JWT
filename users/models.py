from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User Model"""
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=20)
    username = None


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []