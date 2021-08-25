from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import GroupSerializer, CrewSerializer
from .models import  Group, Crew

from rest_framework import status
from rest_framework.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

# feed model 
from feed_api.models import Feed
from feed_api.serializer import FeedSerializer

# Create your views here.
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def makegroup(request):
    leader = request.user.id
    # duplicate = Group.objects.get(group_name = request.data['group_name'])
    # # Group 명 중복 처리
    # print(request)
    # if duplicate != None:
    #     return Response("이미 있는 이름입니다.", status=HTTP_409_CONFLICT)
    # else:
    #     pass
    
    #MARK - make_Group logic
    group_sz = GroupSerializer(data = {"leader":leader, "group_name":request.data['group_name']})
    
    if group_sz.is_valid():
        group_sz.save()
        # return Response(group_sz.data, status=HTTP_201_CREATED)


    #MARK - make_feed logic
    # feed_sz = FeedSerializer(data = {'title':request.data['title'], 'content':request.data['content']}, 'feed_type': request.data['feed_type'])
    try:    
        user = request.user
        feed = Feed(author = user)
        data = {'title':request.data['title'], 'content':request.data['content']}
        feed_sz = FeedSerializer(feed, data = data)  

        return Response('suceess', status= status.HTTP_201_CREATED)
    except:
        return Response('없는 사용자입니다.', status = status.HTTP_404_NOT_FOUND)

    if feed_sz.is_valid():
        feed_sz.save()  
        print("feeds saved")
    else:
        return Response('유효하지 않은 형식입니다.', status = status.HTTP_403_FORBIDDEN)  