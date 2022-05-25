from django.urls import path
from . import views

urlpatterns = [
    path('', views.challenges),
    path('edit/', views.edit)
]
