from django.db import models
from configs.settings import AUTH_USER_MODEL

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=30)

    like_users = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name='like_genres'
    )


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    poster_url = models.TextField()
    overview = models.TextField()

    like_users = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name='like_movies'
    )
    country = models.CharField(max_length=100)
    screentime = models.IntegerField()
    vote_average = models.DecimalField(max_digits=2, decimal_places=1)
    genres = models.JSONField()
    actors = models.JSONField()
    directors = models.JSONField()


class Rating(models.Model):
    score = models.DecimalField(max_digits=2, decimal_places=1)

    user = models.ForeignKey(
        AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
    )

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
    )
