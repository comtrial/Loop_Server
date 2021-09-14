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
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

from feed_api.models import Feed
from group_api.models import Group
from user_api.models import UserCustom

# to custom serilizer
from .serializer import ReportSerializers

# Create your views here.


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def report(request, type, idx):

    try:
        user = request.user
    except:
        return Response('없는 사용자입니다.', status=status.HTTP_404_NOT_FOUND)

    if type == 'user':
        obj_user = UserCustom.objects.get(pk=idx)
        try:
            duplicate = Reports.objects.get(
                reporter=user, object_user=obj_user)
            # Group 명 중복 처리
            if duplicate != None:
                return Response("이미 해당 그룹을 신고하였습니다.", status=HTTP_409_CONFLICT)
            else:
                pass

        except:
            report = Reports(reporter=user,
                             description=request.data['description'], object_user=obj_user)
            report.save()

            report_sz = ReportSerializers(report)
            print('report_sz:', report_sz.data)

            return Response(report_sz.data, status=HTTP_201_CREATED)

    elif type == 'feed':
        feed = Feed.objects.get(pk=idx)
        try:
            duplicate = Reports.objects.get(reporter=user, object_feed=feed)
            # Group 명 중복 처리
            if duplicate != None:
                return Response("이미 해당 그룹을 신고하였습니다.", status=HTTP_409_CONFLICT)
            else:
                pass

        except:
            report = Reports(reporter=user,
                             description=request.data['description'], object_feed=feed)
            report.save()

            report_sz = ReportSerializers(report)
            print('report_sz:', report_sz.data)

            return Response(report_sz.data, status=HTTP_201_CREATED)

    elif type == 'group':
        group = Group.objects.get(pk=idx)
        try:
            duplicate = Reports.objects.get(reporter=user, object_group=group)
            # Group 명 중복 처리
            if duplicate != None:
                return Response("이미 해당 그룹을 신고하였습니다.", status=HTTP_409_CONFLICT)
            else:
                pass

        except:
            report = Reports(reporter=user,
                             description=request.data['description'], object_group=group)
            report.save()

            report_sz = ReportSerializers(report)
            print('report_sz:', report_sz.data)

            return Response(report_sz.data, status=HTTP_201_CREATED)
