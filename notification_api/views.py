from django.shortcuts import render
from .models import Notification
from group_api.models import Group
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from .serializers import  NotificationSerializer

from feed_api.models import Feed

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def read_notification(request):

    user = request.user
    notifications = Notification.objects.filter(to=user)

    notification_sz = NotificationSerializer(notifications, many = True)
    
    return Response(notification_sz.data, status= status.HTTP_201_CREATED)

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def create_group_notification(request):
    user = request.user
    notification_type = request.data['notification_type']

    if notification_type == 'group':
        
        try:    
            group = Group.objects.get(id=request.data['target_idx'])
            to = group.group_leader
            

            notification = Notification(author= user, notification_type= notification_type, to = to, target_idx = group.id)
            notification.save()

            notification_sz = NotificationSerializer(notification)
    
            return Response(notification_sz.data, status= status.HTTP_201_CREATED)

        except:
            return Response('없는 그룹입니다..', status = status.HTTP_404_NOT_FOUND)


def create_feed_notification(request, feed_idx, notification_type):
    user = request.user

    try:    
        feed = Feed.objects.get(id=feed_idx)
        to = feed.author
        

        notification = Notification(author= user, notification_type= notification_type, to = to, target_idx = feed.id)
        notification.save()

        notification_sz = NotificationSerializer(notification)


    except:
        return Response('없는 그룹입니다..', status = status.HTTP_404_NOT_FOUND)
