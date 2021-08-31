from django.urls import path, include
from . import views

urlpatterns = [

    #path('', views.index),
    path('upload', views.upload),
    path('like/<type>/<idx>/', views.like),
    path('home_load', views.home_load),
    path('detail_load/<idx>/', views.detail_load),
    path('delete/<type>/<idx>/', views.delete),
    path('update/<type>/<idx>/', views.update),
    path('comment_upload/<idx>/', views.comment_upload),
    path('cocomment_upload/<idx>/', views.cocomment_upload),


    path('upload_feed/<feed_type>', views.upload),
]