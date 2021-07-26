from .models import Feed
from rest_framework import serializers

class FeedSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = Feed
        fields = ['username', 'title', 'content', 'image']
 
    def get_username_from_author(self, feed):   
        username = feed.author.username
        return username 