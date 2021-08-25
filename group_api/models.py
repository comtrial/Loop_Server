from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Group(models.Model):
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=50, unique=True)
    

class Crew(models.Model):
    crew = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
