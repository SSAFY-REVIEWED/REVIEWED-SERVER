from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie, Rating
from reviews.models import Review
from rest_framework import status
from reviews.serializers import (
    ReviewListSerializer,
)
from .serializers import MovieListSerializer
from accounts.views import get_user

@api_view(['GET',])
def detail(request, movie_pk):
    user = get_user(request.headers)
    movie = get_object_or_404(Movie, pk=movie_pk)

    liked = False
    if movie.like_users.filter(pk=user.id).exists():
        movie.like_users.remove(user)
    else:
        movie.like_users.add(user)
        liked = True

    if Rating.objects.filter(user_id=user.id, movie_id=movie.id).exists():
        rate = Rating.objects.get(user_id=user.id, movie_id=movie.id).score
    else: 
        rate = 0


    serializer = MovieListSerializer(movie).data
    serializer['rate'] = rate
    serializer['like'] = liked

    data = {
        'movieData': serializer,
        'message': '영화를 불러왔습니다.'
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def likes(request, movie_pk):
    user = get_user(request.headers)
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
    user = get_user(request.headers)
    movie = get_object_or_404(Movie, pk=movie_pk)
    rate = request.data['rate']
    if Rating.objects.filter(user_id=user.id, movie_id=movie.id).exists():
        rating = Rating.objects.get(user_id=user.id, movie_id=movie.id)
        rating.delete()

    Rating.objects.create(score = rate, user=user, movie=movie)
    if Review.objects.filter(user_id=user.id, movie_id=movie.id).exists():
        tmp = Review.objects.get(user_id=user.id, movie_id=movie.id)
        tmp.rate = rate
        tmp.save()

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
    user = get_user(request.headers)

    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        review = Review.objects.create(user=user, movie=movie)
        review.title = request.data['reviewTitle']
        review.content = request.data['content']
        review.spoiler = request.data['spoiler']
        if Rating.objects.filter(user_id=user.id, movie_id=movie.id).exists():
            rate = Rating.objects.get(user_id=user.id, movie_id=movie.id).score
        else: 
            rate = 0
        review.rate = rate
        review.save()
        review = ReviewListSerializer(review).data
        message = '리뷰가 성공적으로 생성되었습니다.'
        stat = status.HTTP_201_CREATED

    elif request.method == 'GET':
        try:
            review = Review.objects.filter(user=user).order_by('-id')[0]
            review = ReviewListSerializer(review).data
            message = '리뷰를 성공적으로 로드 했습니다.'
            stat = status.HTTP_200_OK
        except:
            review = {}
            message = '리뷰를 성공적으로 로드 했습니다. 내가 작성한 리뷰 없음'
            stat = status.HTTP_200_OK
    
    reviews = Review.objects.order_by('-id')
    reviews = ReviewListSerializer(reviews, many=True).data
    data = {
        'review': review,
        'reviews': reviews,
        'message': message
    }
    return Response(data, status=stat)

@api_view(['GET'])
def paginator_late(request, movie_pk, page):
    reviews = Review.objects.order_by('-created_at')
    paginator = Paginator(reviews, 10)
    page_obj = paginator.get_page(page)
    serializer = ReviewListSerializer(page_obj, many=True)
    data = {
        'hasMore': bool(paginator.num_pages>page),
        'reviews': serializer.data,
        'message': f'{page} 페이지를 로드 하였습니다'
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def paginator_rate_high(request, movie_pk, page):
    reviews = Review.objects.order_by('-rate')
    paginator = Paginator(reviews, 10)
    page_obj = paginator.get_page(page)
    serializer = ReviewListSerializer(page_obj, many=True)
    data = {
        'hasMore': bool(paginator.num_pages>page),
        'reviews': serializer.data,
        'message': f'{page} 페이지를 로드 하였습니다'
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def paginator_rate_low(request, movie_pk, page):
    reviews = Review.objects.order_by('rate')
    paginator = Paginator(reviews, 10)
    page_obj = paginator.get_page(page)
    serializer = ReviewListSerializer(page_obj, many=True)
    data = {
        'hasMore': bool(paginator.num_pages>page),
        'reviews': serializer.data,
        'message': f'{page} 페이지를 로드 하였습니다'
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def paginator_likes(request, movie_pk, page):
    reviews = Review.objects.order_by('likes')
    paginator = Paginator(reviews, 10)
    page_obj = paginator.get_page(page)
    serializer = ReviewListSerializer(page_obj, many=True)
    data = {
        'hasMore': bool(paginator.num_pages>page),
        'reviews': serializer.data,
        'message': f'{page} 페이지를 로드 하였습니다'
    }
    return Response(data, status=status.HTTP_200_OK)
