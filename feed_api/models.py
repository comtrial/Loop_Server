from django.db import models
# for store user data by authorization
from django.contrib.auth.models import User
from django.conf import settings

#For hastag
# class Tag(TagBase):
#     slug = models.SlugField(verbose_name='slug', unique=True, max_length=100, allow_unicode=True)

# class TaggedFeed(TaggedItemBase):
#     feed = models.ForeignKey('Feed', on_delete=models.CASCADE)
#     tags = models.ForeignKey('Tag', related_name='tagged_feed', on_delete=models.CASCADE)



class Feed(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.AutoField(db_column='id', primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    group_idx = models.IntegerField()
    
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

class Cocomment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', related_name='cocomment', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    feed = models.ForeignKey('Feed', null=True, related_name='like', on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', null=True, related_name='like', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class HashTag(models.Model):
    feed = models.ForeignKey('Feed', related_name='tag', on_delete=models.CASCADE)
    tag = models.CharField(max_length=100)

