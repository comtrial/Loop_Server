from django.urls import path, include
from . import views


urlpatterns = [
    path("create_notification", view=views.create_notification),
    path("read_notification", view=views.read_notification),
]