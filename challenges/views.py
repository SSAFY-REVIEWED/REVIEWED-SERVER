from rest_framework.decorators import api_view, permission_classes
from .models import Challenge
from movies.models import Movie
from accounts.models import User
from .serializers import ChallengeSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

@api_view(['GET'])
def challenges(request):
    challenges = Challenge.objects.all()
    for challenge in challenges:
        pass



@permission_classes([AllowAny])
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def edit(request):
    if request.method == 'GET':
        challenges = Challenge.objects.all()
        serializer = ChallengeSerializer(challenges, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        name = request.data['name']
        reward = request.data['reward']
        mm = request.data['movies']
        movies = list(map(int, mm.split(' ')))
        print(movies)
        challenge = Challenge.objects.create()
        challenge.name = name
        challenge.reward = reward
        challenge.save()
        for id in movies:
            movie = Movie.objects.get(pk=id)
            challenge.listed_movies.add(movie)
        serializer = ChallengeSerializer(challenge).data
        data = {
            'challenge': serializer,
            'message': '성공적으로 생성되었습니다.'
        }
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        challengeId = request.data['challengeId']
        userId = request.data['userId']
        challenge = Challenge.objects.get(pk=challengeId)
        user = User.objects.get(pk=userId)
        challenge.completed_users.add(user)
        data = {
            'message': '성공적으로 유저가 등록 되었습니다.'
        }
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        challengeId = request.data['challengeId']
        challenge = Challenge.objects.get(pk=challengeId)
        challenge.delete()
        data = {
            'message': '성공적으로 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_200_OK)

