from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from configs import settings
import requests
from json.decoder import JSONDecodeError
from .models import User
from .serializers import UserJWTSignupSerializer, UserJWTLoginSerializer

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
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email " + "https://www.googleapis.com/auth/userinfo.profile"
    client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
    return print(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


@api_view(['GET',])
@permission_classes([AllowAny])
def email_validate(request):
    email = request.data['email']
    result = True
    if User.objects.filter(email=email).exists():
        result = False
    data = {
        'result': result
    }
    return JsonResponse(data)
    

@api_view(['GET',])
def profile(request):
    pass


@api_view(['GET',])
def main(request):
    data = {
        'status': 'This is main page'
    }
    return Response(data)

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
                'method': 'signup complete'
            }
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors)

@permission_classes([AllowAny])
class JWTLoginView(APIView):
    serializer_class = UserJWTLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            # user = serializer.validated_data['user']
            access = serializer.validated_data['access']
            refresh = serializer.validated_data['refresh']

            return JsonResponse({
                'access': access,
                'refresh': refresh,
                'method': 'login complete'
            })
        else:
            return JsonResponse(serializer.errors)

            
@api_view(['GET',])
@permission_classes([AllowAny])
def google_callback(request):

    client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
    client_secret = settings.SOCIAL_AUTH_GOOGLE_SECRET
    code = request.GET.get('code')
    state= "random_string"

    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')

    """
    Email Request
    """
    user_info_response = requests.get(
        f"https://www.googleapis.com/oauth2/v1/userinfo?&access_token={access_token}")
    response_status = user_info_response.status_code
    if response_status != 200:
        return JsonResponse({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    user_data = user_info_response.json()
    profile_data = {
            'username': user_data.get('email', ''),
            'first_name': user_data.get('given_name', ''),
            'last_name': user_data.get('family_name', ''),
            'nickname': user_data.get('nickname', ''),
            'name': user_data.get('name', ''),
            'image': user_data.get('picture', None),
            'path': "google",
        }

    return Response(profile_data)
    