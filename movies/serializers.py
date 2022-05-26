from rest_framework import serializers
from .models import Movie, Rating, Genre
from django.db.models import Avg

class MovieSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Movie 
        fields = ('__all__')

class RatingSerializer(serializers.ModelSerializer):

    movieId= serializers.SerializerMethodField()
    movieTitle = serializers.SerializerMethodField()
    posterUrl = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    
    class Meta():
        model = Rating 
        fields = ('movieId', 'movieTitle', 'posterUrl', 'rate')

    def get_movieId(self,  obj):
        movie = obj.movie
        return movie.id
    def get_movieTitle(self,  obj):
        movie = obj.movie
        return movie.title
    def get_posterUrl(self,  obj):
        movie = obj.movie
        return f'https://image.tmdb.org/t/p/w500{movie.poster_url}'
    def get_rate(self,  obj):
        return obj.score


class MovieListSerializer(serializers.ModelSerializer):
    movieId = serializers.IntegerField(source="pk")
    releaseDate = serializers.DateField(source="release_date")
    screenTime = serializers.IntegerField(source="screentime")

    voteAverage = serializers.SerializerMethodField()
    posterUrl = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()


    class Meta():
        model = Movie 
        fields = (
            'movieId', 'title', 'releaseDate',
            'posterUrl', 'genres', 'actors',
            'country', 'directors', 'screenTime',
            'overview', 'voteAverage', 'rate', 'like',
        )

    def get_voteAverage(self,  obj):
        ratings = obj.rating_set.all()
        tmp = ratings.all().aggregate(a=Avg('score'))
        if not tmp['a']:
            tmp['a'] = 0.0
        return tmp['a']

    def get_posterUrl(self,  obj):
        return f'https://image.tmdb.org/t/p/w500{obj.poster_url}'

    def get_rate(self,  obj):
        return ''

    def get_like(self,  obj):
        return ''

class MovieMainSerializer(serializers.ModelSerializer):

    movieId= serializers.SerializerMethodField()
    movieTitle = serializers.SerializerMethodField()
    posterUrl = serializers.SerializerMethodField()
    voteAverage = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    
    class Meta():
        model = Movie 
        fields = ('movieId', 'movieTitle', 'posterUrl', 'genres', 'voteAverage', 'like')

    def get_movieId(self,  obj):
        return obj.id

    def get_movieTitle(self,  obj):
        return obj.title

    def get_voteAverage(self,  obj):
        ratings = obj.rating_set.all()
        tmp = ratings.aggregate(a=Avg('score'))
        if not tmp['a']:
            tmp['a'] = 0.0
        return tmp['a']

    def get_posterUrl(self,  obj):
        return f'https://image.tmdb.org/t/p/w500{obj.poster_url}'

    def get_like(self,  obj):
        return False