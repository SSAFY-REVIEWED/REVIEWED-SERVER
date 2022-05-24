from django.urls import path
from . import views

urlpatterns = [
    path('<int:movie_pk>/', views.detail),

    path('<int:movie_pk>/likes/', views.likes),

    path('<int:movie_pk>/ratings/', views.ratings),

    path('<int:movie_pk>/reviews/', views.reviews),
    
    path('<int:movie_pk>/reviews/late/<int:page>/', views.paginator_late),

    path('<int:movie_pk>/reviews/rate-high/<int:page>/', views.paginator_rate_high),
    
    path('<int:movie_pk>/reviews/rate-low/<int:page>/', views.paginator_rate_low),

    path('<int:movie_pk>/reviews/likes/<int:page>/', views.paginator_likes),
]
