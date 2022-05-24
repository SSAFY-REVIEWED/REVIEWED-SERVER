from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie, Rating
from reviews.models import Review
from accounts.models import User
from .serializers import MovieSerializer
from rest_framework import status
import jwt
from reviews.serializers import (
    ReviewListSerializer
)

@api_view(['GET',])
def detail(request, movie_pk):
    access_token = request.headers.get('Authorization', None)[7:]
    payload = jwt.decode(access_token, verify=False)
    user = User.objects.get(id=payload['user_id'])
    movie = get_object_or_404(Movie, pk=movie_pk)
    ratings = movie.rating_set.all()
    rate = 0
    if ratings:
        if ratings.filter(user_id=user.id).exists():
            rating = Rating.objects.get(user_id=user.id)
            rate = rating.score
        total = 0
        for t in ratings:
            total += t.score
        ea = movie.rating_set.count()
        if total:
            avg = total / ea
    else:
        avg = 0

    liked = False
    if movie.like_users.filter(pk=user.id).exists():
        movie.like_users.remove(user)
    else:
        movie.like_users.add(user)
        liked = True

    movie = MovieSerializer(movie).data
    moviedata = {
        'movieId': movie['id'], 
        'title': movie['title'],
        'releaseDate': movie['release_date'],
        'posterUrl': 'https://image.tmdb.org/t/p/w500' + movie['poster_url'],
        'genres': movie['genres'],
        'actors': movie['actors'],
        'country': movie['country'],
        'directors': movie['directors'],
        'screenTime': movie['screentime'],
        'overview': movie['overview'],
        'voteAverage': avg,
        'rate': rate,
        'like': liked,
        }

    data = {
        'movieData': moviedata,
        'message': '영화를 불러왔습니다.'
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def likes(request, movie_pk):
    access_token = request.headers.get('Authorization', None)[7:]
    payload = jwt.decode(access_token, verify=False)
    user = User.objects.get(id=payload['user_id'])
    movie = get_object_or_404(Movie, pk=movie_pk)
    response = {
        'message': '좋아요',
        "liked": False,
    }   

    if movie.like_users.filter(pk=user.id).exists():
        movie.like_users.remove(user)
        response['message'] = '좋아요 취소'
    else:
        movie.like_users.add(user)
        response["liked"] = True

    return Response(response, status=status.HTTP_200_OK)

@api_view(['POST'])
def ratings(request, movie_pk):
    access_token = request.headers.get('Authorization', None)[7:]
    payload = jwt.decode(access_token, verify=False)
    user = User.objects.get(id=payload['user_id'])

    movie = get_object_or_404(Movie, pk=movie_pk)
    rate = request.data['rate']
    if Rating.objects.filter(user_id=user.id).exists():
        rating = Rating.objects.filter(user_id=user.id)
        rating.delete()

    Rating.objects.create(score = rate, user=user, movie=movie)

    total = 0
    tmp = movie.rating_set.all()
    for t in tmp:
        total += t.score
    ea = movie.rating_set.count()
    avg = total / ea

    context = {
        'message': '평점 부여 완료',
        'rates': avg
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def reviews(request, movie_pk):
    access_token = request.headers.get('Authorization', None)[7:]
    payload = jwt.decode(access_token, verify=False)
    user = User.objects.get(id=payload['user_id'])

    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        review = Review.objects.create(user=user, movie=movie)
        review.title = request.data['title']
        review.content = request.data['content']
        review.spoiler = request.data['spoiler']
        review.save()
        review = ReviewListSerializer(review).data
        message = '리뷰가 성공적으로 생성되었습니다.'
        stat = status.HTTP_201_CREATED

    else:
        try:
            review = Review.objects.filter(user=user).order_by('-id')[0]
            review = ReviewListSerializer(review).data
            message = '리뷰를 성공적으로 로드 했습니다.'
            stat = status.HTTP_200_OK
        except:
            review = {}
            message = '리뷰를 성공적으로 로드 했습니다. 내가 작성한 리뷰 없음'
            stat = status.HTTP_200_OK

    reviews = Review.objects.all().order_by('-id')[1:5]
    reviews = ReviewListSerializer(reviews, many=True).data
    data = {
        'review': review,
        'reviews': reviews,
        'message': message
    }
    return Response(data, status=stat)