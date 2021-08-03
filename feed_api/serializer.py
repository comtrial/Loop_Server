from .models import Feed, Image
from rest_framework import serializers



class ImageSeriallizer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image']    
    


class FeedSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')
    feed_image = ImageSeriallizer(many = True, read_only = True)

    class Meta:
        model = Feed
        fields = ['id', 'username', 'title', 'content', 'feed_image']
 
    def get_username_from_author(self, feed):   
        username = feed.author.username
        return username 
    
    def get_images(self, obj):
        image = obj.image_set.all()
        return ImageSeriallizer(image, many=True).data
