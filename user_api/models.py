from django.db import models
from .department import DEPARTMENT
# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

DEPARTMENT_CHOICES = (DEPARTMENT.items())

class UserCustom(AbstractUser):#이미 makemigrations-migrate를 한경우AbstractUser가 적용이 안됨 auth_user를 다 설계한 이후에 migrations절차 진행 요망
    department = models.IntegerField(default=0, choices=DEPARTMENT_CHOICES)
    class Meta:
        db_table = "auth_user"

        
# token 형성 logic
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created: 
#         Token.objects.create(user = instance)