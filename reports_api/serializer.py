from .models import Reports
from rest_framework import serializers
from .models import Reports

# for group feed
from group_api.models import Group

class ReportSerializers(serializers.ModelSerializer):

    class Meta:
        model = Reports
        fields = ['id', 'author_id', 'username', 'title', 'tag', 'created_at', 'content', 'feed_image', 'feed_comment', 'like', 'group_idx']