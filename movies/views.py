from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


def detail(request, movie_pk):
    # 영화 리스트 pagination 으로 넘기기
    pass

def likes(request, movie_pk):
    pass

def ratings(request, movie_pk):
    pass

def reviews(request, movie_pk):
    # 리뷰 리스트 내거 상단 + 다른사람리뷰 (좋아요 순 4개)
    pass