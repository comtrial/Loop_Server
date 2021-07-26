from django.urls import path
from . import views

urlpatterns = [
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
]