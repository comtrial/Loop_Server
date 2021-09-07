from django.urls import path, include
from . import views


urlpatterns = [
    path("create_group_notification", view=views.create_group_notification),
    path("read_notification", view=views.read_notification),
]