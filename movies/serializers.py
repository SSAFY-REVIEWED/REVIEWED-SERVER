from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Movie 
        fields = ('__all__')

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
        if ratings:
            total = 0
            for rating in ratings:
                total += rating.score
            ea = obj.rating_set.count()
            if total:
                avg = total / ea
        else:
            avg = 0.0
        return round(avg, 1)

    def get_posterUrl(self,  obj):
        return f'https://image.tmdb.org/t/p/w500{obj.poster_url}'

    def get_rate(self,  obj):
        return ''

    def get_like(self,  obj):
        return ''
