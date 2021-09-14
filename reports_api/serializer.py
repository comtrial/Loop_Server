from .models import Reports
from rest_framework import serializers
from .models import Reports

# for group feed
from group_api.models import Group


class ReportSerializers(serializers.ModelSerializer):

    class Meta:
        model = Reports
        fields = ['reporter', 'object_user', 'object_feed',
                  'object_group', 'description', 'date']
