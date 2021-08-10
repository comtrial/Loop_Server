from django.db import models
# for store user data by authorization
from django.contrib.auth.models import User
from django.conf import settings

class Feed(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.AutoField(db_column='id', primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    # feed_img = models.ForeignKey('Image', on_delete=models.CASCADE)
    #content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FeedImage(models.Model):
    feed = models.ForeignKey('Feed', related_name='feed_image', on_delete=models.CASCADE)
    image = models.ImageField(null=True)

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    feed = models.ForeignKey('Feed', related_name='feed_comment', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)    

class Like(models.Model):
    feed = models.ForeignKey('Feed', null=True, related_name='like', on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', null=True, related_name='like', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

