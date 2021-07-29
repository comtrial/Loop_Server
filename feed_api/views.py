from django.shortcuts import render
from .models import Feed, Image
from django.core.paginator import Paginator  
from django.http import HttpResponse

# to custom rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 

# to custom serilizer
from .serializer import FeedSerializer, ImageSeriallizer

# Create your views here.


# feed upload 처리
# input: {
#   username: 
#   password:
#   title:
#   content:
#   feed_img: option
# }
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def upload(request):

    # err 처리 ex)
    # try:
    #     pass
    # except Feed.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == "POST":
        user = request.user
        feed = Feed(author = user)
        data = request.data
        feed_sz = FeedSerializer(feed, data = {'username':data['username'], 
                                                  'title':data['title'], 
                                                'content':data['content']})  
        if feed_sz.is_valid():
            feed_sz.save()        

        if data['image'] != '':
            print(data['image'])
            print(type(data['image']))
            feed_id = feed_sz.data['id']

            image_sz = ImageSeriallizer(data = {'feed_id':feed_id, 
                                                  'image':data['image']})
            if image_sz.is_valid():
                image_sz.save()
        # for image in data['image']:
        #     response_id = 0
        #     image_sz = ImageSeriallizer(data={'image':image})
        #     if image_sz.is_valid():
        #         response_id = 1
        #         image_sz.save()
                return Response({"feed_data":feed_sz.data, "image_data":image_sz.data}, status=status.HTTP_201_CREATED)
            else:
                print("유효한형식이 아님")
        else:
            response_id = 1
        if response_id == 1:
            
            return Response(feed_sz.data, status=status.HTTP_201_CREATED)
        return Response(feed_sz.errors, status=status.HTTP_400_BAD_REQUEST)

# serialize 해 줄 꺼면 many = True 해줘서 진행해야할듯 
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