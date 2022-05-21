from django.urls import path
from . import views

urlpatterns = [
    path('reviews/<int:review_pk>/', views.detail),

    path('reviews/<int:review_pk>/likes', views.likes),

    path('reviews/<int:review_pk>/comments', views.comments),

    path('reviews/<int:review_pk>/comments/<int:comment_pk>', views.update),
]
