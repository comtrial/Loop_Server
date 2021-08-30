
from django.db.models.fields import files
from .models import Notification
from rest_framework import serializers

class NotificationSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = Notification
        # fields = '__all__'

        fields = ['id', 'username','author_id', 'target_idx', 'to_id', 'notification_type']

    def get_username_from_author(self, notification):   
        username = notification.author.username
        return username 