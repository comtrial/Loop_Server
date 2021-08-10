from django.urls import path, include
from . import views

urlpatterns = [

    #path('', views.index),
    path('upload', views.upload),
    path('like/<type>/<idx>/', views.like),
    path('home_load', views.home_load),
    path('detail_load/<idx>/', views.detail_load),
    path('comment_upload/<idx>/', views.comment_upload)
]