from django.urls import path, include
from . import views

urlpatterns = [
    path('upload', views.upload),
    path('home_load', views.home_load),
    path('detail_load/<idx>/', views.detail_load)
]