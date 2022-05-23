from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Genre

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=100, default='')
    profile_img = models.ImageField(default='profile-placeholder.png')
    exp = models.IntegerField(default=0)
    bio = models.TextField(max_length=100, null=True)
    survey = models.ForeignKey(Genre, on_delete = models.CASCADE, null=True)
