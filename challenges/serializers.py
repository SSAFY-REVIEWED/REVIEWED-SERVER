from rest_framework import serializers
from .models import Challenge
from movies.models import Movie
from django.db.models import Avg

class ChallengeSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Challenge
        fields = ('__all__')

class MovieChallengerSerializer(serializers.ModelSerializer):

    movieTitle = serializers.SerializerMethodField()
    movieId = serializers.SerializerMethodField()
    posterUrl = serializers.SerializerMethodField()
    voteAverage = serializers.SerializerMethodField()
    reviewed = serializers.SerializerMethodField()
    
    class Meta():
        model = Movie 
        fields = ('movieTitle', 'movieId', 'posterUrl', 'voteAverage', 'reviewed')

    def get_movieTitle(self,  obj):
        return obj.title

    def get_movieId(self,  obj):
        return obj.id

    def get_voteAverage(self,  obj):
        ratings = obj.rating_set.all()
        tmp = ratings.aggregate(a=Avg('score'))
        if not tmp['a']:
            tmp['a'] = 0.0
        return tmp['a']

    def get_posterUrl(self,  obj):
        return f'https://image.tmdb.org/t/p/w500{obj.poster_url}'

    def get_reviewed(self,  obj):
        return True
        