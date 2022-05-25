from django.urls import path
from . import views

urlpatterns = [
    path('<int:movie_pk>/', views.detail),

    path('<int:movie_pk>/likes/', views.likes),

    path('<int:movie_pk>/ratings/', views.ratings),

    path('<int:movie_pk>/reviews/', views.reviews),

]
