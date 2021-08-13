from django.shortcuts import render
from django.core.paginator import Paginator 

from .models import Notice, NoticeImage
from .serializer import NoticeSerializer, ImageSerializer

from rest_framework import response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 

from django.contrib.auth import get_user_model
# Create your views here.

@api_view(['POST', ])
# @permission_classes((IsAuthenticated,))
def upload(request):
    User = get_user_model()
    try:
        user = request.user
        notice = Notice(author=user)
        department = user.department
        data = {'title':request.data['title'], 'content':request.data['content'], 'department':department, 'url':request.data['url']}
        notice_sz = NoticeSerializer(notice, data = data)
    
    except:
        return Response('wrong user', status = status.HTTP_401_UNAUTHORIZED)

    if notice_sz.is_valid():     
        notice_sz.save()
    else:
        return Response('wrong post form', status = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        
    notice = Notice.objects.get(pk=notice_sz.data['id'])

    try:
        for image in request.FILES.getlist('image'):
            NoticeImage.objects.create(notice=notice, image = image)
    except:
        return Response('유효하지 않은 형식입니다.', status = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
                    
    return Response(notice_sz.data, status=status.HTTP_201_CREATED)

@api_view(['GET', ])
# @permission_classes((IsAuthenticated,))
def home_load(request):
    
    # Model에서 data get
    try:
        notice = Notice.objects.all()
    except Notice.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Serializer 을 통한 response 구성
    if request.method == "GET":

        ## # 페이징처리

        # 입력 파라미터
        page = request.GET.get('page')  # 페이지
        # 페이징처리
        paginator = Paginator(notice, 3)  # 페이지당 3개씩 보여주기
        page_obj = paginator.get_page(page)
        print(page_obj.end_index())# 총 피드 개수

        ## # 페이징처리
        serializer = NoticeSerializer(page_obj, many = True)
          
        return Response(serializer.data)
    


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def detail_load(request, idx):
    
    # Model에서 data get
    try:

        notice = Notice.objects.get(id = idx)
        
    except Notice.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Serializer 을 통한 response 구성
    if request.method == "GET":
        print(notice.author.date_joined)
        serializer = NoticeSerializer(notice)
        return Response(serializer.data)