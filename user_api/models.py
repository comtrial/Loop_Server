from django.db import models
from .department import DEPARTMENT
# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

DEPARTMENT_CHOICES = (DEPARTMENT.items())


class UserCustom(AbstractUser):
    # 이미 makemigrations-migrate를 한경우AbstractUser가 적용이 안됨 auth_user를 다 설계한 이후에 migrations절차 진행 요망
    department = models.IntegerField(default=0, choices=DEPARTMENT_CHOICES)

    class Meta:
        db_table = "auth_user"


class Profile(models.Model):
    # nickname = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='feed_comment', on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='author_pk')
    nickname = models.CharField(max_length=100, default='user_id')
    profile_image = models.ImageField(null=True)
    grade = models.CharField(max_length=100, default='신입생')

    # 혹시 몰라 추가하는 field lists
    class_num = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100)

    class Meta:
        db_table = "auth_user_profile"


class Customizing(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.AutoField(db_column='id', primary_key=True)
    type = models.CharField(max_length=100)
    contents = models.TextField()
    seq_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "auth_user_customizing"

    # def __str__(self):
    #     return self.title
# ↓
# ↑


class Customizing_imgs(models.Model):
    customizing = models.ForeignKey(
        'Customizing', related_name='customizing_image', on_delete=models.CASCADE)
    image = models.ImageField(null=True)

    class Meta:
        db_table = "auth_user_customizing_imgs"
# token 형성 logic
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user = instance)
