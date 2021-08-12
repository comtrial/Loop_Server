from django.urls import path
from . import views

urlpatterns = [
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup_checkemail/', views.signup_checkemail, name='signup_checkemail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('activate/<str:uidb64>/<str:token>', views.Activate.as_view(), name = 'activate_email'),
    path('getlist/', views.get_list, name='getlist'),
]