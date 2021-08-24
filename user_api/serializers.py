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
                  'grade', 'class_num', 'real_name']


class Customizing_imgs_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Customizing_imgs
        fields = ['customizing', 'image']


class CustomizingSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_author')
    customizing_image = Customizing_imgs_Serializer(many=True, read_only=True)

    class Meta:
        model = Customizing
        fields = ['id', 'username', 'type', 'contents',
                  'created_at', 'customizing_image']

    def get_username_from_author(self, customizing):
        username = customizing.author.username
        return username
