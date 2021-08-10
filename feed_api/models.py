from django.db import models
# for store user data by authorization
from django.contrib.auth.models import User
from django.conf import settings
class Feed(models.Model):
    # on_delete=models.CASCADE : 작성자 탈퇴시 게시글 삭제
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.AutoField(db_column='id', primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    like = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Image(models.Model):
    feed = models.ForeignKey('Feed', related_name='feed_image', on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    
    # def __str__(self):
    #     return self.image

