from django.urls import path
from . import views

urlpatterns = [
    path('<int:review_pk>/', views.detail),

    path('<int:review_pk>/likes/', views.likes),

    path('<int:review_pk>/comments/', views.comments),

    path('<int:review_pk>/comments/<int:comment_pk>/', views.update),
]
