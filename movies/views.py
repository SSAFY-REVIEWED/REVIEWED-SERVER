from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg
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
        tmp = Review.objects.filter(user_id=user.id, movie_id=movie.id)[0]
        tmp.rate = rate
        tmp.save()

    avg = movie.rating_set.all().aggregate(a=Avg('score'))['a']
    if not avg:
        avg = 0.0

    context = {
        'message': '평점 부여 완료',
        'voteAverage': avg
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def reviews(request, movie_pk):
    user = get_user(request.headers)
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        if Review.objects.filter(user=user, movie=movie).exists():
            review = Review.objects.filter(user=user, movie=movie).order_by('-id')[0]
        else:
            review = Review.objects.create(user=user, movie=movie)
        review.title = request.data['reviewTitle']
        review.content = request.data['content']
        if request.data.get('spoiler') == 'true':
            review.spoiler = True
        else:
            review.spoiler = False
        if Rating.objects.filter(user=user, movie=movie).exists():
            rate = Rating.objects.get(user=user, movie=movie).score
        else: 
            rate = 0
        review.rate = rate
        review.save()
        review = ReviewListSerializer(review).data
        message = '리뷰가 성공적으로 생성되었습니다.'
        user.exp += 10
        user.save()
        stat = status.HTTP_201_CREATED

    elif request.method == 'GET':
        # 쿼리검색 페이지네이터
        if request.GET.get('query'):
            movie = get_object_or_404(Movie, pk=movie_pk)
            query = request.GET['query']
            if query == 'late':
                query = '-created_at'
            elif query == 'rate-high':
                query = '-rate'
            elif query == 'rate-low':
                query = 'rate'
            else:
                query = 'likes'
            page = int(request.GET['page'])
            reviews = movie.review_set.order_by(query)
            paginator = Paginator(reviews, 10)
            page_obj = paginator.get_page(page)
            serializer = ReviewListSerializer(page_obj, many=True).data
            for i in range(len(page_obj)):
                if page_obj[i].like_users.filter(pk=user.id).exists():
                    serializer[i]['like'] = True
            data = {
                'hasMore': bool(paginator.num_pages>page),
                'reviews': serializer,
                'message': f'{query} 검색 {page} 페이지를 로드 하였습니다'
            }
            return Response(data, status=status.HTTP_200_OK)

        if Review.objects.filter(user=user, movie=movie_pk).exists():
            review_og = Review.objects.filter(user=user, movie=movie_pk).order_by('-id')[0]
            rate = 0
            if Rating.objects.filter(user=user, movie=movie).exists():
                rate = Rating.objects.get(user=user, movie=movie).score
            review_og.rate = rate
            review_og.save()
            review = ReviewListSerializer(review_og).data
            if review_og.like_users.filter(pk=user.id).exists():
                review['like'] = True
            message = '리뷰를 성공적으로 로드 했습니다.'
            stat = status.HTTP_200_OK
        else:
            review = {}
            message = '리뷰를 성공적으로 로드 했습니다. 내가 작성한 리뷰 없음'
            stat = status.HTTP_200_OK

    serializer = {}
    if Review.objects.filter(movie=movie).order_by('-id').exists():
        reviews = Review.objects.filter(movie_id=movie_pk).exclude(user_id=user.id).order_by('-id')[:4]
        serializer = ReviewListSerializer(reviews, many=True).data
        for i in range(len(reviews)):
            if reviews[i].like_users.filter(pk=user.id).exists():
                serializer[i]['like'] = True
    data = {
        'review': review,
        'reviews': serializer,
        'message': message
    }
    return Response(data, status=stat)

