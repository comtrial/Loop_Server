from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Group(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    group_leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=10, unique=True)
    group_description = models.CharField(max_length=50)
    
    def __str__(self):
        return self.group_name

class GroupImage(models.Model):
    group = models.ForeignKey('Group', related_name='group_image', on_delete=models.CASCADE)
    image = models.ImageField(null=True)

class Crew(models.Model):
    crew = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey('Group', related_name='crew',on_delete=models.CASCADE)

