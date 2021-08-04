from .models import Feed, FeedImage, Comment, CommentImage
from rest_framework import serializers



class CommentImageSeriallizer(serializers.ModelSerializer):
    
    class Meta:
        model =  CommentImage
        fields = ['image']

class FeedImageSeriallizer(serializers.ModelSerializer):

    class Meta:
        model = FeedImage
        fields = ['image']  
    
class CommentSerializer(serializers.ModelSerializer):
    
    username = serializers.SerializerMethodField('get_username_from_author')
    comment_image = CommentImageSeriallizer(many = True, read_only = True)

    class Meta:
        model = Comment
        fields = ['id', 'feed', 'username', 'content', 'created_at', 'comment_image']
    
    def get_username_from_author(self, feed):   
        username = feed.author.username
        return username 

class FeedSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')
    feed_image = FeedImageSeriallizer(many = True, read_only = True)
    feed_comment = CommentSerializer(many = True, read_only = True)

    class Meta:
        model = Feed
        fields = ['id', 'username', 'title', 'created_at', 'content', 'feed_image', 'feed_comment']
 
    def get_username_from_author(self, feed):   
        username = feed.author.username
        return username 
    
    # def get_images(self, obj):
    #     image = obj.image_set.all()
    #     return ImageSeriallizer(image, many=True).data
