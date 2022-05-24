from django.shortcuts import get_object_or_404
from .models import Review, Comment
from accounts.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ReviewListSerializer,
    CommentListSerializer
)
import jwt

from reviews import serializers
# Create your views here.
@api_view(['GET', 'PATCH', 'DELETE'])
def detail(request, review_pk):
    if request.method == 'GET':
        review = get_object_or_404(Review, pk=review_pk)
        serializer = ReviewListSerializer(review)
        data = {
            'review': serializer.data,
            'message': '리뷰를 불러왔습니다.',
        }
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        review = get_object_or_404(Review, pk=review_pk)
        review.title = request.data['reviewTitle']
        review.content = request.data['content']
        review.spoiler = request.data['spoiler']
        review.save()
        serializer = ReviewListSerializer(review)
        data = {
            'review': serializer.data,
            'message': '리뷰를 성공적으로 수정했습니다.',
        }
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        review = get_object_or_404(Review, pk=review_pk)
        review.delete()
        data = {
            'message': '리뷰를 성공적으로 삭제했습니다.',
        }
        return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def likes(request, review_pk):
    access_token = request.headers.get('Authorization', None)[7:]
    payload = jwt.decode(access_token, verify=False)
    user = User.objects.get(id=payload['user_id'])
    review = get_object_or_404(Review, pk=review_pk)
    response = {
        'message': '좋아요',
        "liked": False,
    }   

    if review.like_users.filter(pk=user.id).exists():
        review.like_users.remove(user)
        response['message'] = '좋아요 취소'
    else:
        review.like_users.add(user)
        response["liked"] = True

    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def comments(request, review_pk):
    access_token = request.headers.get('Authorization', None)[7:]
    payload = jwt.decode(access_token, verify=False)
    user = User.objects.get(id=payload['user_id'])
    review = get_object_or_404(Review, pk=review_pk)
    message = '덧글을 성공적으로 불러왔습니다.'

    if request.method == 'POST':
        comment = Comment.objects.create(review=review, user=user)
        comment.content = request.data['content']
        comment.save()
        message = '덧글이 성공적으로 생성되었습니다.'

    comments = review.comment_set.all()
    serializer = CommentListSerializer(comments, many=True)
    data = {
        'replyCounts': review.comment_set.count(),
        'comments': serializer.data,
        'message': message
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['PATCH', 'DELETE'])
def update(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    message = ''
    if request.method == 'PATCH':
        comment.content = request.data['content']
        comment.save()
        message = '덧글이 성공적으로 수정되었습니다.'
    if request.method == 'DELETE':
        comment.delete()
        message = '덧글이 성공적으로 삭제되었습니다.'

    comments = review.comment_set.all()
    serializer = CommentListSerializer(comments, many=True)
    data = {
        'replyCounts': review.comment_set.count(),
        'comments': serializer.data,
        'message': message
    }
    return Response(data, status=status.HTTP_200_OK)
