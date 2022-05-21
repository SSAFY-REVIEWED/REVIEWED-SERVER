from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # name = models.CharField(max_length=30)
    profile_img = models.ImageField(null=True)
    exp = models.IntegerField(default=0)
    bio = models.TextField(max_length=100, null=True)

