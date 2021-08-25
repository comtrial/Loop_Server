from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Feed, FeedImage, Comment, Like, HashTag
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
from .serializer import FeedSerializer, CommentSerializer, LikeSerializer, HashTagSerializer, FeedImageSerializer

# UPLOAD
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def like(request, type, idx):
    user = request.user
    like = Like(author = user)
    if type == 'feed':
        try: 
            like_valid = Like.objects.get(feed_id=idx, author_id = user.id)
            like_valid.delete()
            return Response('disliked feed', status = status.HTTP_202_ACCEPTED)
        except:
            like_sz = LikeSerializer(like, data={'feed':idx})
            if like_sz.is_valid():
                like_sz.save()
                return Response('liked feed', status = status.HTTP_202_ACCEPTED)
    if type == 'comment':
        try: 
            like_valid = Like.objects.get(comment_id=idx, author_id = user.id)
            like_valid.delete()
            return Response('disliked comment', status = status.HTTP_202_ACCEPTED)
        except:
            like_sz = LikeSerializer(like, data={'comment':idx})
            if like_sz.is_valid():
                like_sz.save()
                return Response('liked comment', status = status.HTTP_202_ACCEPTED)
    

@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def upload(request):
        
    if request.method == "POST":

        try:    
            user = request.user
            # print("user:", user)
            # print("user_type:", type(user))
            feed = Feed(author = user)
            # print("feed_type:", type(feed))
            data = {'title':request.data['title'], 'content':request.data['content']}
            feed_sz = FeedSerializer(feed, data = data)
            # print("feed_sz:", feed_sz)  

        except:
            return Response('없는 사용자입니다.', status = status.HTTP_404_NOT_FOUND)

        if feed_sz.is_valid():
            feed_sz.save()  
        else:

            return Response('유효하지 않은 형식입니다.', status = status.HTTP_403_FORBIDDEN)   
        
        try:
            for image in request.FILES.getlist('image'):
                image_sz = FeedImageSerializer(data = {'feed':feed_sz.data['id'], 'image':image})
                print('feed_image_sz:', image_sz)
                if image_sz.is_valid():
                    print('이건 벨리드지')
                    image_sz.save()
        except:
            return Response('유효하지 않은 형식입니다.', status = status.HTTP_403_FORBIDDEN)

        for tag in request.data['hashtag'].split('#'):
            if tag != '':
                tag_sz = HashTagSerializer(data = {'feed':feed_sz.data['id'], 'tag':tag})
                if tag_sz.is_valid():
                    tag_sz.save()

        feed = Feed.objects.get(pk=feed_sz.data['id'])  
        feed_sz = FeedSerializer(feed)   

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
 
        comment_sz = CommentSerializer(user, data = {'feed':idx, 'content':request.data['content']})

        if comment_sz.is_valid():
            comment_sz.save()
        else:

            return Response('유효하지 않은 형식입니다.', status = status.HTTP_403_FORBIDDEN)       

        return Response(comment_sz.data, status = status.HTTP_201_CREATED)

#UPDATE
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def update(request, type, idx):

    if type == 'feed':
        feed = Feed.objects.get(pk=idx)
        feed.title = request.data['title']
        feed.content = request.data['content']
        feed.save()

        tag = HashTag.objects.filter(feed_id = feed.id)
        tag.delete()

        for tag in request.data['hashtag'].split('#'):
            if tag != '':
                tag_sz = HashTagSerializer(data = {'feed':feed.id, 'tag':tag})
                if tag_sz.is_valid():
                    tag_sz.save()
    
    if type == 'comment':
        comment = Comment.objects.get(pk = idx)
        comment.content = request.data['content']
        comment.save()
        

#DELETE
@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def delete(request, type, idx):
    user = request.user.id 
    if type == "feed":
        feed = Feed.objects.get(pk = idx)
        if feed.author_id == user:
            feed.delete()
    
    if type == "comment":
        comment = Comment.objects.get(pk = idx)
        if comment.author_id == user:
            comment.delete()


#LOAD
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def home_load(request):
    # Model에서 data get
    try:
        feeds = Feed.objects.all().order_by('-id')
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
        # print(page_obj.end_index())# 총 피드 개수

        ## # 페이징처리
        serializer = FeedSerializer(page_obj, many = True)
        for data in serializer.data:
            try:
                liked = Like.objects.get(feed_id=data['id'], author_id=request.user.id)
                data.update({'feed_liked':1})
            except:
                pass

            if data['username'] == request.user.username:
                data.update({'is_author':1})
            
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
 
        serializer = FeedSerializer(feed)

        for comment in serializer.data['feed_comment']:
            try:
                liked = Like.objects.get(comment_id=comment['id'], author_id=request.user.id)
                comment.update({'comment_liked':1})
            except:
                pass

            if comment['username'] == request.user.username:
                comment.update({'is_author':1})

        return_dict = {}
        return_dict.update(serializer.data)

        if serializer.data['username'] == request.user.username:
            return_dict.update({'is_author' : 1})

        try:
            liked = Like.objects.get(feed_id=idx, author_id=request.user.id)
            return_dict.update({'feed_liked' : 1})

        except:
            pass

        return Response(return_dict)