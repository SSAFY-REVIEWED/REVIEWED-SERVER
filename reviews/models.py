from django.db import models
from configs.settings import AUTH_USER_MODEL
from movies.models import Movie
from configs import settings

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    spoiler = models.BooleanField(default=False)

    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
    )

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_reviews'
    )


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
    )

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )


class Cocomment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )