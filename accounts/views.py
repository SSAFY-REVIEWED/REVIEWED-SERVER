from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from accounts.models import User
from movies.models import Movie, Genre
from .serializers import (
    UserJWTSignupSerializer, 
    UserJWTLoginSerializer,
    UserSerializer,
    UserMiniSerializer,
    UserSearchSerializer,
    UserRankingSerializer
)
from movies.serializers import RatingSerializer, MovieMainSerializer
from reviews.serializers import ReviewListSerializer, ReviewDateSerializer, ReviewGenreSerializer
import jwt


BASE_URL = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'api/v1/google/callback/'

# 헤더에서 유저객체 가져오기
def get_user(token):
    access_token = token.get('Authorization', None)[7:]
    payload = jwt.decode(access_token, verify=False)
    user = User.objects.get(id=payload['user_id'])
    return user

# 레벨계산
def level(exp):
    if exp < 100:
        return 'Iron', round((exp/100)*100, 1)
    elif exp < 400:
        return 'Bronze', round((exp-100)/600*100, 1)
    elif exp < 1000:
        return 'Silver', round((exp-1000)/1000*100, 1)
    elif exp < 2000:
        return 'Gold', round((exp-2000)/2000*100, 1)
    elif exp < 4000:
        return 'Platinum', round((exp-2000)/3000*100, 1)
    elif exp < 7000:
        return 'Diamond', round((exp-4000)/3000*100, 1)
    elif exp < 12000:
        return 'Master', round((exp-7000)/5000*100, 1)
    elif exp < 20000:
        return 'Grandmaster', round((exp-12000)/8000*100, 1)
    elif exp >= 20000:
        return 'Challenger', 100

'''
------------------------------
# 프로필 페이지
------------------------------
'''

@api_view(['GET'])
def user_info(request):
    user = get_user(request.headers)
    if user:
        data = {
            'name': user.name,
            'userId': user.id,
            'profileImg': f'/media/{user.profile_img}',
            'survey': user.survey_genre,
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def profile(request, user_pk):
    if request.method == 'GET':
        me = get_user(request.headers)
        user = get_object_or_404(User, pk=user_pk)
        serializer = UserSerializer(user).data
        if me.followings.filter(pk=user.id).exists():
            serializer['follow'] = True
        lv, per = level(user.exp)
        serializer['level'] = lv
        serializer['levelImg'] = f'/media/{lv}.jpg'
        serializer['levelPercentage'] = per
        return Response(serializer, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        user = get_object_or_404(User, pk=user_pk)
        if request.data.get('name'):
            user.name = request.data['name']
        if request.FILES.get('profileImg'): 
            user.profile_img = request.FILES['profileImg']
        if request.data.get('bio'):
            user.bio = request.data['bio']
        user.save()
        serializer = UserSerializer(user).data
        lv, per = level(user.exp)
        serializer['level'] = lv
        serializer['levelImg'] = f'/media/{lv}.jpg'
        serializer['levelPercentage'] = per
        return Response(serializer, status=status.HTTP_200_OK)

@api_view(['GET'])
def history(request, user_pk):
    value = []
    value2 = []
    value3 = []
    cal = {}
    all_genres = {
        "모험": 0, "판타지": 0, "애니메이션": 0, "드라마": 0, "공포": 0,
        "액션": 0, "코미디": 0, "역사": 0, "서부": 0, "스릴러": 0,
        "범죄": 0, "다큐멘터리": 0, "SF": 0, "미스터리": 0, "음악": 0,
        "로맨스": 0, "가족": 0, "전쟁": 0, "TV 영화": 0
    }
    user = get_object_or_404(User, pk=user_pk)
    reviews = user.review_set.all()
    dates = ReviewDateSerializer(reviews, many=True).data
    genres = ReviewGenreSerializer(reviews, many=True).data
    challenge = user.completed_challenges.all()
    for c in challenge:
        value3.append(c.name)
    for date in dates:
        key = date['createdAt']
        try: cal[key] += 1
        except: cal[key] = 1
    for k, v in cal.items():
        tmp = dict()
        tmp['date'] = k
        tmp['count'] = v
        value.append(tmp)
    for genre in genres:
        for i in genre['genres']:
            all_genres[i] += 1
    for k, v in all_genres.items():
        tmp = dict()
        tmp['genre'] = k
        tmp['count'] = v
        value2.append(tmp)

    data = {
        'reviewDateCountList': value,
        'reviewGenreCountList': value2,
        'Challenges': value3,
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def reviews(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    reviews = user.review_set.all()
    page = int(request.GET.get('page'))
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
def movies(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    rates = user.rating_set.all()
    page = int(request.GET.get('page'))
    paginator = Paginator(rates, 10)
    page_obj = paginator.get_page(page)
    serializer = RatingSerializer(page_obj, many=True)
    data = {
        'hasMore': bool(paginator.num_pages>page),
        'movies': serializer.data,
        'message': f'{page} 페이지를 로드 하였습니다'
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def following(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    followings = user.followings.all()
    serializers = UserMiniSerializer(followings, many=True).data
    return Response(serializers, status=status.HTTP_200_OK)

@api_view(['GET'])
def followed(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    followers = user.followers.all()
    serializers = UserMiniSerializer(followers, many=True).data
    return Response(serializers, status=status.HTTP_200_OK)

def cancel(request, user_pk, target_pk):
    target = get_object_or_404(User, pk=target_pk)
    user = get_object_or_404(User, pk=user_pk)
    user.followers.remove(target)
    response = {
        "message": '팔로우중인 유저를 삭제하였습니다',
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def follow(request, user_pk, target_pk):
    target = get_object_or_404(User, pk=target_pk)
    user = get_object_or_404(User, pk=user_pk)

    response = {
        "followed": False,
    }

    if target.followers.filter(pk=user.pk).exists():
        target.followers.remove(user)
    else:
        target.followers.add(user)
        response["followed"] = True

    return Response(response, status=status.HTTP_200_OK)

'''
------------------------------
# 로그인, 회원가입, 서베이
------------------------------
'''

@api_view(['GET','POST'])
@permission_classes([AllowAny])
def email_validate(request):
    email = request.data['email']
    if User.objects.filter(email=email).exists():
        data = {
            'message': "중복된 이메일이 존재합니다."
        }
        return Response(data, status=status.HTTP_409_CONFLICT)
    else:
        data = {
            'message': "사용가능한 이메일 주소입니다."
        }
        return Response(data, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def survey(request):
    user = get_user(request.headers)
    survey = request.data['preferenceGenreList'] # 장르 한글명만 담아서
    user.survey_genre = survey
    user.save()
    data = {
            'message': "선호 장르 선택이 완료되었습니다."
        }
    return Response(data, status=status.HTTP_202_ACCEPTED)

'''
------------------------------
# 메인 페이지, 서치, 랭킹
------------------------------
'''

@api_view(['GET',])
@permission_classes([AllowAny])
def intro(request):
    return


@api_view(['GET',])
def search(request):
    user = get_user(request.headers)
    query = request.GET.get('query')
    type = request.GET.get('type')
    if type == 'movies':
        movies = Movie.objects.filter(title__icontains=query)
        serializers = MovieMainSerializer(movies, many=True).data
        for movie in serializers:
            m_id = movie.get('movieId')
            tmp = Movie.objects.get(pk=m_id)
            liked = False
            if tmp.like_users.filter(pk=user.id).exists():
                liked = True
            movie['like'] = liked
        return Response(serializers, status=status.HTTP_200_OK)
    elif type == 'users':
        targets = User.objects.filter(name__icontains=query).exclude(id=user.id)
        serializers = UserSearchSerializer(targets, many=True).data
        for target in serializers:
            t_id = target.get('userId')
            tmp = get_object_or_404(User, pk=t_id)
            if tmp.followers.filter(pk=user.id).exists():
                target['follow'] = True
        return Response(serializers, status=status.HTTP_200_OK)


@api_view(['GET',])
def ranking(request):
    users = User.objects.order_by('-exp')[:15]
    serializers = UserRankingSerializer(users, many=True).data
    for user in serializers:
        experi = user['exp']
        lv, per = level(experi)
        user['level'] = lv
        user['levelImg'] = f'/media/{lv}.jpg'
    return Response(serializers, status=status.HTTP_200_OK)


@api_view(['GET',])
def main(request):
    user = get_user(request.headers)
    total = {}

    tmp = {}
    tmp['name'] = 'TMDB 평점 TOP 10 영화'
    movies = Movie.objects.order_by('-vote_average')[:10]
    serializers = MovieMainSerializer(movies, many=True).data
    for k in range(10):
        if movies[k].like_users.filter(pk=user.id).exists():
            serializers[k]['like'] = True
    tmp['movieList'] = serializers
    total['top10'] = tmp

    tmp = {}
    tmp['name'] = '최근 인기있는 영화'
    movies = Movie.objects.order_by('-release_date')[:10]
    serializers = MovieMainSerializer(movies, many=True).data
    for k in range(10):
        if movies[k].like_users.filter(pk=user.id).exists():
            serializers[k]['like'] = True
    tmp['movieList'] = serializers
    total['lately'] = tmp

    survey = user.survey_genre
    survey = set(survey[1:len(survey)-1].split(','))
    for i in survey:
        tmp = {}
        tmp['name'] = f'{i} 장르 추천영화'
        movies = Movie.objects.filter(genres__0__name=i).order_by('?')[:10]
        serializers = MovieMainSerializer(movies, many=True).data
        for k in range(10):
            if movies[k].like_users.filter(pk=user.id).exists():
                serializers[k]['like'] = True
        tmp['movieList'] = serializers
        total[i] = tmp
    return Response(total, status=status.HTTP_200_OK)


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
                'message': '아이디 또는 비밀번호를 확인해주세요'
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
        'profileImg': user_data.get('picture', None),
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