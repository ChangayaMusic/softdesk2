# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    age = models.IntegerField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)
    birthday = models.DateField(null=True, blank=True)

