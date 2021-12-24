from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=64)
    is_doctor = models.BooleanField()
    is_patient = models.BooleanField()
    REQUIRED_FIELDS = ['name', 'is_doctor', 'is_patient']
