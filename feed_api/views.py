from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Feed, FeedImage, Comment, CommentImage
from django.core.paginator import Paginator  
from django.http import HttpResponse

# to custom rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 

# to custom serilizer
from .serializer import FeedSerializer, FeedImageSeriallizer, CommentSerializer

# Create your views here.

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def upload(request):
        
    if request.method == "POST":

        try:
            user = request.user
            feed = Feed(author = user)
            data = {'title':request.POST['title'], 'content':request.POST['content']}
            feed_sz = FeedSerializer(feed, data = data)  
        except:
            return Response('없는 사용자입니다.', status = status.HTTP_404_NOT_FOUND)

        if feed_sz.is_valid():
            feed_sz.save()  
        else:
            return Response('유효하지 않은 형식입니다.', status = status.HTTP_403_FORBIDDEN)   

        feed = Feed.objects.get(pk=feed_sz.data['id'])

        try:
            for image in request.FILES.getlist('image'):
                FeedImage.objects.create(feed=feed, image = image)
        except:
            return Response('유효하지 않은 형식입니다.', status = status.HTTP_403_FORBIDDEN)
                      
        return Response(feed_sz.data, status=status.HTTP_201_CREATED)

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def comment_upload(request, idx):
    if request.method == "POST":
        try:
            user = request.user
            user = Comment(author = user)
            
        except:
            return Response('없는 사용자입니다.', status = status.HTTP_404_NOT_FOUND)
 
        comment_sz = CommentSerializer(user, data = {'feed':idx, 'content':request.POST['content']})

        if comment_sz.is_valid():
            comment_sz.save()

        else:

            return Response('유효하지 않은 형식입니다.', status = status.HTTP_403_FORBIDDEN)   

        comment = Comment.objects.get(pk=comment_sz.data['id'])
        
        try:
            for image in request.FILES.getlist('image'):
  
                CommentImage.objects.create(comment=comment, image = image)
        except:

            return Response('유효하지 않은 형식입니다.', status = status.HTTP_403_FORBIDDEN)

        return Response(comment_sz.data, status = status.HTTP_201_CREATED)
        

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def home_load(request):
    
    # Model에서 data get
    try:
        feeds = Feed.objects.all()
    except Feed.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Serializer 을 통한 response 구성
    if request.method == "GET":

        ## # 페이징처리

        # 입력 파라미터
        page = request.GET.get('page')  # 페이지
        # 페이징처리
        paginator = Paginator(feeds, 3)  # 페이지당 3개씩 보여주기
        page_obj = paginator.get_page(page)
        print(page_obj.end_index())# 총 피드 개수

        ## # 페이징처리
        serializer = FeedSerializer(page_obj, many = True)
          
        return Response(serializer.data)
    


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def detail_load(request, idx):
    
    # Model에서 data get
    try:

        feed = Feed.objects.get(id = idx)
        
    except Feed.DoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Serializer 을 통한 response 구성
    if request.method == "GET":
        print(feed.author.date_joined)
        serializer = FeedSerializer(feed)
        return Response(serializer.data)