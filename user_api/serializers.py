from .models import UserCustom
from .models import UserCustom, Profile, Customizing, Customizing_imgs
from rest_framework import serializers


class UserCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = ['department']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['nickname', 'profile_image',
                  'class_num', 'real_name']


class Customizing_imgs_Serializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = Customizing_imgs
        fields = ['customizing', 'username', 'image']

    def get_username_from_author(self, customizing):
        username = customizing.author.username
        return username


class CustomizingSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')
    customizing_image = Customizing_imgs_Serializer(many=True, read_only=True)

    class Meta:
        model = Customizing
        fields = ['id', 'username', 'type', 'contents', 'customizing_image',
                  'created_at', 'seq_id']

    def get_username_from_author(self, customizing):
        username = customizing.author.username
        return username
