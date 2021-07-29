from .models import Feed, Image
from rest_framework import serializers



class ImageSeriallizer(serializers.ModelSerializer):

    # id = serializers.SerializerMethodField('get_feed_id')

    class Meta:
        model = Image
        fields = ['feed_id', 'image']    
    # def get_feed_id(self, image):
    #     feed_id = image.feed.id
    #     return feed_id

class FeedSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')
    feed_image = ImageSeriallizer(many = True, read_only = True)

    class Meta:
        model = Feed
        fields = ['id', 'username', 'title', 'content', 'feed_image']
 
    def get_username_from_author(self, feed):   
        username = feed.author.username
        return username 