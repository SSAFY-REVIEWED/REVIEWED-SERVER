from rest_framework import serializers
from .models import Review, Comment

class ReviewListSerializer(serializers.ModelSerializer):
    reviewId = serializers.IntegerField(source="id")
    userId = serializers.IntegerField(source="user_id")
    reviewTitle = serializers.CharField(source="title")
    createdAt = serializers.DateTimeField(source="created_at")
    movieId = serializers.IntegerField(source="movie_id")
    viewCount = serializers.IntegerField(source="views")

    movieTitle = serializers.SerializerMethodField()
    userProfileImg = serializers.SerializerMethodField()
    userName = serializers.SerializerMethodField()
    posterUrl = serializers.SerializerMethodField()
    voteAverage = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    replyCount = serializers.SerializerMethodField()


    class Meta():
        model = Review
        fields = (
            'reviewId', 'reviewTitle', 'content', 'createdAt',
            'userId', 'userProfileImg', 'userName',
            'movieId', 'movieTitle', 'posterUrl', 'spoiler',
            'voteAverage', 'rate',
            'likes', 'like', 'replyCount', 'viewCount',
        )

    def get_userProfileImg(self,  obj):
        user = obj.user
        return f'/media/{user.profile_img}'

    def get_userName(self,  obj):
        user = obj.user
        return f'{user.name}'

    def get_movieTitle(self, obj):
        movie = obj.movie
        return f'{movie.title}'

    def get_posterUrl(self,  obj):
        movie = obj.movie
        return f'https://image.tmdb.org/t/p/w500{movie.poster_url}'

    def get_voteAverage(self,  obj):
        movie = obj.movie
        return movie.vote_average

    def get_like(self,  obj):
        user = obj.user
        like = False
        if obj.like_users.filter(id=user.id).exists():
            like = True
        else:
            like = False
        return like

    def get_replyCount(self,  obj):
        counts = obj.comment_set.count()
        return counts


class CommentListSerializer(serializers.ModelSerializer):

    commentId = serializers.IntegerField(source="pk")
    userId = serializers.IntegerField(source="user_id")
    createdAt = serializers.DateTimeField(source="created_at")

    userProfileImg = serializers.SerializerMethodField()
    userName = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'commentId', 'userId', 'userProfileImg',
            'userName', 'content', 'createdAt',
        )

    def get_userProfileImg(self,  obj):
        user = obj.user
        return f'{user.profile_img}'
    
    def get_userName(self,  obj):
        user = obj.user
        return f'{user.name}'