# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    
    age = models.IntegerField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)
    birthday = models.DateField(null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
