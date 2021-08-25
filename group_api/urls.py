from django.urls import path
from . import views

urlpatterns = [

    path('make_group/', views.makegroup),

]