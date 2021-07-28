from .models import UserCustom
from rest_framework import serializers

class UserCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = ['department']