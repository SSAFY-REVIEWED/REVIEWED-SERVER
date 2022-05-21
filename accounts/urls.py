from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from . import views

urlpatterns = [
    # 가입하지 않은 사용자에게 허용되는 첫 화면
    path('', views.intro),

    # 로그인 한 사용자 첫화면 (메인)
    path('main/', views.main),

    # 로그인, 회원가입
    path('login/', views.JWTLoginView.as_view()),
    path('signup/', views.JWTSignupView.as_view()),
    path('email/', views.email_validate),

    # JWT 토큰 access 재발급
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # 프로필 페이지
    path('profile/<int:user_pk>/', views.profile),
    path('profile/<int:user_pk>/history/', views.history),
    path('profile/<int:user_pk>/reviews/', views.reviews),
    path('profile/<int:user_pk>/following/', views.following),
    path('profile/<int:user_pk>/followed/', views.followed),
    path('profile/<int:user_pk>/following/<int:target_pk>/', views.cancel),
    path('profile/<int:user_pk>/follow/<int:target_pk>/', views.follow),

    # # google 로그인
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    # path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
]
