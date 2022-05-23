from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from configs import settings
from .models import User
from movies.models import Movie
from .serializers import (
    UserJWTSignupSerializer, 
    UserJWTLoginSerializer,
)
import jwt


BASE_URL = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'api/v1/google/callback/'

# Create your views here.
@api_view(['GET',])
@permission_classes([AllowAny])
def intro(request):
    return render(request, 'accounts/index.html')

@api_view(['GET',])
@permission_classes([AllowAny])
def google_login(request):
    scope = "https://www.googleapis.com/auth/userinfo.email " + "https://www.googleapis.com/auth/userinfo.profile"
    client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


@api_view(['GET',])
@permission_classes([AllowAny])
def email_validate(request):
    email = request.data['email']
    if User.objects.filter(email=email).exists():
        data = {
            'message': "사용가능한 이메일 주소입니다."
        }
        return JsonResponse(data, status=status.HTTP_202_ACCEPTED)
    else:
        data = {
            'message': "중복된 이메일이 존재합니다."
        }
        return JsonResponse(data, status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
def survey(request):
    pass


@api_view(['GET',])
def user_info(request):
    access_token = request.headers.get('Authorization', None)[7:]
    if access_token:
        payload = jwt.decode(access_token, verify=False)
        user = User.objects.get(id=payload['user_id'])
        data = {
            'name': user.first_name + user.last_name,
            'user_id': user.id,
            'profile_img': '/media/' + str(user.profile_img),
            'survey': user.survey_genre,
        }
        return Response(data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

'''
------------------------------
# 메인 페이지
------------------------------
'''

@api_view(['GET',])
def main(request):
    movies = Movie.objects.all()
    length = movies.count()
    results = {}
    for i in range(length):
        movie = movies[i]
        rates = movie.rating_set.all()
        genres = movie.survey_genre
        if not rates:
            rates = 0
        if rates:
            avg = sum(rates)/len(rates)
        else:
            avg = 0.0
        data = {
            'id': movie.id, 
            'title': movie.title,
            'poster_url': 'https://image.tmdb.org/t/p/w500' + movie.poster_url,
            'genres': genres,
            'rates': avg,
        }
        results[i] = data
    return Response(results, status=status.HTTP_200_OK)

'''
------------------------------
# 프로필 페이지
------------------------------
'''

@api_view(['GET',])
def profile(request):
    pass

def history(request):
    return

def reviews(request):
    return
    
def following(request):
    return

def followed(request):
    return

def cancel(request):
    return

def follow(request):
    return

'''
------------------------------
# JWT 인증 토큰 (로그인, 회원가입)
------------------------------
'''

@permission_classes([AllowAny])
class JWTSignupView(APIView):
    serializer_class = UserJWTSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            user = serializer.save(request)
            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            data = {
                'access': access,
                'refresh': refresh,
                'message': '회원가입 성공'
            }
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message': serializer.errors
            }
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN)


@permission_classes([AllowAny])
class JWTLoginView(APIView):
    serializer_class = UserJWTLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            access = serializer.validated_data['access']
            refresh = serializer.validated_data['refresh']
            
            data = {
                'access': access,
                'refresh': refresh,
                'message': '로그인 성공'
            }

            return JsonResponse(data, status=status.HTTP_202_ACCEPTED)
        else:
            data = {
                'message': serializer.errors
            }
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN)


'''
------------------------------
# 구글 로그인 콜백 (로그인, 회원가입)
------------------------------
'''

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def google_callback(request):

    credential = request.data['credential']
    user_data = jwt.decode(credential, verify=False)
    
    email = user_data.get('email', '')
    profile_data = {
        'email': user_data.get('email', ''),
        'name': user_data.get('name', ''),
        'profile_img': user_data.get('picture', None),
        'password': 'googleAuth'
        }

    if User.objects.filter(email=email).exists():
        serializer = UserJWTLoginSerializer(data=profile_data)

        if serializer.is_valid(raise_exception=False):
            access = serializer.validated_data['access']
            refresh = serializer.validated_data['refresh']
            
            data = {
                'access': access,
                'refresh': refresh,
                'message': '로그인 성공'
            }

            return JsonResponse(data, status=status.HTTP_202_ACCEPTED)
        else:
            data = {
                'message': serializer.errors
            }
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN)

    else:
        serializer = UserJWTSignupSerializer(data=profile_data)

        if serializer.is_valid(raise_exception=False):
            user = serializer.save(request)
            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            data = {
                'access': access,
                'refresh': refresh,
                'message': '회원가입 성공'
            }
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message': serializer.errors
            }
            return JsonResponse(data, status=status.HTTP_403_FORBIDDEN)