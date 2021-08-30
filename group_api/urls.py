from django.urls import path
from . import views

urlpatterns = [

    path('create_group/', views.create_group),
    path('create_crew/<group_idx>', views.create_crew),
    path('read_group/<group_idx>', views.read_group),
]