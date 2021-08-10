from django.db import models
from django.conf import settings
# Create your models here.

class Notice(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    notice_url = models.TextField()
    department = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class NoticeImage(models.Model):
    notice = models.ForeignKey('Notice', related_name='notice_image', on_delete=models.CASCADE)
    image = models.ImageField(null=True)