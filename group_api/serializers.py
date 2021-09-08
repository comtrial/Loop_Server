from django.db.models import fields
from .models import  Group, Crew, GroupImage
from rest_framework import serializers



class CrewSerializer(serializers.ModelSerializer):

    crewname = serializers.SerializerMethodField('get_userInfo')
    class Meta:
        model = Crew
        fields = ['crew', 'crewname','group']
    
    def get_userInfo(self, crew):
        
        username = crew.crew.username 
        return username

    def get_userProfile(self, crew):
        
        userProfile = crew.crew.username 

        return username


class GroupImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupImage
        fields = ['group', 'image']  



class GroupSerializer(serializers.ModelSerializer):

    crew = CrewSerializer(many = True, read_only = True)
    # group_image = GroupImageSerializer(read_only = True)

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'group_image','group_description', 'group_leader', 'crew']
        