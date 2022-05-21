from django.db import models
from configs.settings import AUTH_USER_MODEL
from movies.models import Movie


# Create your models here.
class Challenge(models.Model):
    name = models.CharField(max_length=100)
    reward = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    completed_users = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name='completed_challenges'
    )

    listed_movies = models.ManyToManyField(
        Movie,
        related_name='listed_challenges'
    )