from django.db.models.fields import files
from .models import Feed, FeedImage, Comment, Like, HashTag, Cocomment
from rest_framework import serializers
from user_api.models import Profile

# for group feed
from group_api.models import Group

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

class CocommentSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = Cocomment
        fields = ['id', 'comment', 'username','content', 'created_at']
    
    def get_username_from_author(self, comment):   
        username = comment.author.username
        return username 
    
class CommentSerializer(serializers.ModelSerializer):

    cocomment = CocommentSerializer(many = True, read_only = True)
    username = serializers.SerializerMethodField('get_username_from_author')
    like = LikeSerializer(many = True, read_only = True)

    class Meta:
        model = Comment
        fields = ['id', 'feed', 'username', 'content', 'created_at', 'like', 'cocomment', 'author_id']
    
    def get_username_from_author(self, comment):   
        username = comment.author.username
        return username 

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['profile_image', 'nickname']

class FeedSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')
    feed_image = FeedImageSerializer(many = True, read_only = True)
    feed_comment = CommentSerializer(many = True, read_only = True)
    like = LikeSerializer(many = True, read_only = True)
    tag = HashTagSerializer(many = True, read_only = True)
    # tags = TagListSerializerField()

    class Meta:
        model = Feed
        fields = ['id', 'author_id', 'username', 'title', 'tag', 'created_at', 'content', 'feed_image', 'feed_comment', 'like', 'group_idx']
 
    def get_username_from_author(self, feed):  
        username = feed.author.username
        return username 
    
    # def get_images(self, obj):
    #     image = obj.image_set.all()
    #     return ImageSeriallizer(image, many=True).data


class FeedGroupSerialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['feed', 'group_idx']  