from django.db.models import fields
from .models import Notice, NoticeImage
from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeImage
        fields = ['image']
    
class NoticeSerializer(serializers.ModelSerializer):
    notice_image = ImageSerializer(many=True, read_only=True)

    class Meta:
        department = serializers.SerializerMethodField('get_department')
        model = Notice
        fields = ['id', 'department', 'title', 'content', 'notice_url','notice_image', 'department']

        def get_department(self, notice):
            department = notice.author.department
            return department