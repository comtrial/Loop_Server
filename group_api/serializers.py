from django.db.models import fields
from .models import  Group, Crew
from rest_framework import serializers

class CrewSerializer(serializers.ModelSerializer):

    group_name = serializers.SerializerMethodField('get_groupname_from_author')

    class Meta:
        model = Crew
        fields = ['group_name']
    
    def get_groupname_from_author(self, group):   
        group_name = group.group_name
        return group_name 

class GroupSerializer(serializers.ModelSerializer):

    crew = CrewSerializer(many = True, read_only = True)

    class Meta:
        model = Group
        fields = ['id', 'group_name', 'leader', 'crew']