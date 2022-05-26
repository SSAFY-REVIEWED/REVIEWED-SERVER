from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # 가입하지 않은 사용자에게 허용되는 첫 화면
    path('', views.intro),

    # 로그인 한 사용자 첫화면 (메인)
    path('main/', views.main),
    
    # 유저정보
    path('user-info/', views.user_info),
    path('survey/', views.survey),
    path('search/', views.search),
    path('ranking/', views.ranking),
    path('recommend/', views.recommend),


    # 로그인, 회원가입
    path('login/', views.JWTLoginView.as_view()),
    path('signup/', views.JWTSignupView.as_view()),
    path('email/', views.email_validate),

    # JWT 토큰 access 재발급
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 프로필 페이지
    path('profile/<int:user_pk>/', views.profile),
    path('profile/<int:user_pk>/history/', views.history),
    path('profile/<int:user_pk>/reviews/', views.reviews),
    path('profile/<int:user_pk>/movies/', views.movies),

    # 팔로우/팔로잉
    path('profile/<int:user_pk>/following/', views.following),
    path('profile/<int:user_pk>/followed/', views.followed),
    path('profile/<int:user_pk>/followed/<int:target_pk>/', views.cancel),
    path('profile/<int:user_pk>/following/<int:target_pk>/', views.follow),

    # google 로그인
    path('google/callback/', views.google_callback, name='google_callback'),
]
