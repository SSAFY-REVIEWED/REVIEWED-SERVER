from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie, Rating
from accounts.models import User
from .serializers import MovieSerializer
from rest_framework import status
import jwt


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
    movieData = {
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
        'movieData': movieData,
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

def reviews(request, movie_pk):
    # 리뷰 리스트 내거 상단 + 다른사람리뷰 (좋아요 순 4개)
    pass
