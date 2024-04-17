from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
# Create your models here.

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, default=None)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username