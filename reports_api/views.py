from django.shortcuts import render

from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.utils.serializer_helpers import ReturnDict
from .models import Reports
from user_api.models import Profile
from django.core.paginator import Paginator
from django.http import HttpResponse

# to custom rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

# to custom serilizer
# from .serializer import ReportSerializers

# Create your views here.
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def report(request, type, idx):
    user = request.user
    report = Reports(reporter=user)
    print("report:", report)
    # if type == 'feed':
    #     try:
    #         like_valid = Like.objects.get(feed_id=idx, author_id=user.id)
    #         like_valid.delete()
    #         return Response('disliked feed', status=status.HTTP_202_ACCEPTED)
    #     except:
    #         like_sz = LikeSerializer(like, data={'feed': idx})
    #         if like_sz.is_valid():
    #             like_sz.save()
    #             return Response('liked feed', status=status.HTTP_202_ACCEPTED)
    # if type == 'comment':
    #     try:
    #         like_valid = Like.objects.get(comment_id=idx, author_id=user.id)
    #         like_valid.delete()
    #         return Response('disliked comment', status=status.HTTP_202_ACCEPTED)
    #     except:
    #         like_sz = LikeSerializer(like, data={'comment': idx})
    #         if like_sz.is_valid():
    #             like_sz.save()
    #             return Response('liked comment', status=status.HTTP_202_ACCEPTED)