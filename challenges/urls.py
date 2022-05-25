from django.urls import path
from . import views

urlpatterns = [
    path('', views.challenges),
    path('auth/', views.edit)
]
