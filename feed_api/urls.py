from django.urls import path, include
from . import views

urlpatterns = [

    #path('', views.index),
    path('upload', views.upload),
    # path('upload', views.FeedViewSet),
    path('home_load', views.home_load),
    path('detail_load/<idx>/', views.detail_load)
]