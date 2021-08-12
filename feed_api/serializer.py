from django.db.models.fields import files
from .models import Feed, FeedImage, Comment, Like, HashTag
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

class HashTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = HashTag
        fields = ['feed', 'tag']

class LikeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = Like
        # fields = ['username']
        fields = ['username', 'feed', 'comment']
    
    def get_username_from_author(self, feed):   
        username = feed.author.username
        return username 

class FeedImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedImage
        fields = ['feed', 'image']  
    
class CommentSerializer(serializers.ModelSerializer):
    
    username = serializers.SerializerMethodField('get_username_from_author')
    like = LikeSerializer(many = True, read_only = True)

    class Meta:
        model = Comment
        fields = ['id', 'feed', 'username', 'content', 'created_at', 'like']
    
    def get_username_from_author(self, feed):   
        username = feed.author.username
        return username 

class FeedSerializer(TaggitSerializer, serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')
    feed_image = FeedImageSerializer(many = True, read_only = True)
    feed_comment = CommentSerializer(many = True, read_only = True)
    like = LikeSerializer(many = True, read_only = True)
    tag = HashTagSerializer(many = True, read_only = True)
    # tags = TagListSerializerField()

    class Meta:
        model = Feed
        fields = ['id', 'username', 'title', 'tag', 'created_at', 'content', 'feed_image', 'feed_comment', 'like']
 
    def get_username_from_author(self, feed):   
        username = feed.author.username
        return username 
    
    # def get_images(self, obj):
    #     image = obj.image_set.all()
    #     return ImageSeriallizer(image, many=True).data
