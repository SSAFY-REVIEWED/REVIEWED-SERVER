from django.shortcuts import get_object_or_404
from .models import Review, Comment
from accounts.models import User
from movies.models import Rating
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ReviewListSerializer,
    CommentListSerializer
)
from accounts.views import get_user

@api_view(['GET', 'PATCH', 'DELETE'])
def detail(request, review_pk):
    user = get_user(request.headers)
    if request.method == 'GET':
        review = get_object_or_404(Review, pk=review_pk)
        review.views += 1
        review.save()
        serializer = ReviewListSerializer(review).data
        if review.like_users.filter(pk=user.id).exists():
            serializer['like'] = True
        data = {
            'review': serializer,
            'message': '리뷰를 불러왔습니다.',
        }
        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        review = get_object_or_404(Review, pk=review_pk)
        if request.data.get('reviewTitle'):
            review.title = request.data['reviewTitle']
        if request.data.get('content'):
            review.content = request.data['content']
        if request.data.get('spoiler'):
            review.spoiler = bool(request.data['spoiler'])
        review.save()
        serializer = ReviewListSerializer(review).data
        if review.like_users.filter(pk=user.id).exists():
            serializer['like'] = True
        data = {
            'review': serializer,
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
    user = get_user(request.headers)
    review = get_object_or_404(Review, pk=review_pk)
    response = {
        'message': '좋아요',
        "liked": False,
    }   

    if review.like_users.filter(pk=user.id).exists():
        review.like_users.remove(user)
        response['message'] = '좋아요 취소'
        review.likes -= 1
    else:
        review.like_users.add(user)
        response["liked"] = True
        review.likes += 1
    review.save()
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def comments(request, review_pk):
    user = get_user(request.headers)
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
