from django.urls import path
from . import views

urlpatterns = [

    path('create_group/', views.create_group),
    path('create_crew/<group_idx>', views.create_crew),
    path('read_group/<group_idx>', views.read_group),
    path('group_profile_update/<idx>', views.group_profile_update),
    path('read_all_groups/', views.read_all_groups),
    path('get_user_groups/', views.get_user_groups)
]