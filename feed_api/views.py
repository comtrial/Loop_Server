from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.utils.serializer_helpers import ReturnDict
from .models import Feed, FeedImage, Comment, Like, HashTag, Cocomment
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
from .serializer import FeedSerializer, CommentSerializer, LikeSerializer, HashTagSerializer, FeedImageSerializer, CocommentSerializer, UserProfileSerializer
from user_api.serializers import ProfileSerializer

# to notification 
import notification_api.views as notification_api


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def like(request, type, idx):
    user = request.user
    like = Like(author=user)
    if type == 'feed':
        try:
            like_valid = Like.objects.get(feed_id=idx, author_id=user.id)
            like_valid.delete()
            return Response('disliked feed', status=status.HTTP_202_ACCEPTED)
        except:
            like_sz = LikeSerializer(like, data={'feed': idx})
            if like_sz.is_valid():
                like_sz.save()
                return Response('liked feed', status=status.HTTP_202_ACCEPTED)
    if type == 'comment':
        try:
            like_valid = Like.objects.get(comment_id=idx, author_id=user.id)
            like_valid.delete()
            return Response('disliked comment', status=status.HTTP_202_ACCEPTED)
        except:
            like_sz = LikeSerializer(like, data={'comment': idx})
            if like_sz.is_valid():
                like_sz.save()
                return Response('liked comment', status=status.HTTP_202_ACCEPTED)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def upload(request):

    if request.method == "POST":

        try:
            user = request.user
            feed = Feed(author=user)
            data = {'title': request.data['title'],
                    'content': request.data['content'],
                    'group_idx': user.department}####????????? ?????? ??? ??????!! ??????!!!!
            feed_sz = FeedSerializer(feed, data=data)

        except:
            return Response('?????? ??????????????????.', status=status.HTTP_404_NOT_FOUND)

        if feed_sz.is_valid():
            feed_sz.save()

        else:
            
            return Response('???????????? ?????? ???????????????.', status=status.HTTP_403_FORBIDDEN)

        try:
            for image in request.FILES.getlist('image'):
                image_sz = FeedImageSerializer(
                    data={'feed': feed_sz.data['id'], 'image': image})
                if image_sz.is_valid():
                    image_sz.save()
        except:
            return Response('???????????? ?????? ???????????????.', status=status.HTTP_403_FORBIDDEN)

        try:
            for tag in request.data['hashtag'].split('#'):
                if tag != '':
                    tag_sz = HashTagSerializer(
                        data={'feed': feed_sz.data['id'], 'tag': tag})
                    if tag_sz.is_valid():
                        tag_sz.save()
        
        except:
            pass

        return Response('????????? ??????', status=status.HTTP_201_CREATED)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def comment_upload(request, idx):

    user = request.user

    try:
        profile = Profile.objects.get(author=user.id)
        profile_sz = ProfileSerializer(profile)
        user = Comment(author=user)
        comment_sz = CommentSerializer(
            user, data={'feed': idx, 'content': request.data['content']})
    except:
        return Response('?????? ??????????????????.', status=status.HTTP_404_NOT_FOUND)

    if comment_sz.is_valid():
        comment_sz.save()
        notification_api.create_feed_notification(request, idx, 'comment')
    else:

        return Response('???????????? ?????? ???????????????.', status=status.HTTP_403_FORBIDDEN)

    return_dict = {
        "id": comment_sz.data['id'],
        "feed": comment_sz.data['feed'],
        "username": comment_sz.data['username'],
        "content": comment_sz.data['content'],
        "created_at": comment_sz.data['created_at'],
        "cocomment": comment_sz.data['cocomment'],
        "author_id": comment_sz.data['author_id'],
        "profile_image": profile_sz.data['profile_image']
    }

    return Response(return_dict, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def cocomment_upload(request, idx):

    user = request.user

    try:
        user = Cocomment(author=user)
        comment_sz = CocommentSerializer(
            user, data={'comment': idx, 'content': request.data['content']})
    except:
        return Response('?????? ??????????????????.', status=status.HTTP_404_NOT_FOUND)

    if comment_sz.is_valid():
        comment_sz.save()
        notification_api.create_feed_notification(request, idx, 'comment')
    else:

        return Response('???????????? ?????? ???????????????.', status=status.HTTP_403_FORBIDDEN)

    return Response(comment_sz.data, status=status.HTTP_201_CREATED)

# UPDATE


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def update(request, type, idx):

    if type == 'feed':
        feed = Feed.objects.get(pk=idx)
        feed.title = request.data['title']
        feed.content = request.data['content']
        feed.save()

        tag = HashTag.objects.filter(feed_id=feed.id)
        tag.delete()

        for tag in request.data['hashtag'].split('#'):
            if tag != '':
                tag_sz = HashTagSerializer(data={'feed': feed.id, 'tag': tag})
                if tag_sz.is_valid():
                    tag_sz.save()

        feed_sz = FeedSerializer(feed)

        return Response('?????? ???????????? ??????', status=status.HTTP_202_ACCEPTED)

    if type == 'comment':
        comment = Comment.objects.get(pk=idx)
        comment.content = request.data['content']
        comment.save()
        comment_sz = CommentSerializer(comment)
        return Response(comment_sz.data, status=status.HTTP_202_ACCEPTED)

    if type == 'cocomment':
        comment = Cocomment.objects.get(pk=idx)
        comment.content = request.data['content']
        comment.save()
        comment_sz = CommentSerializer(comment)
        return Response(comment_sz.data, status=status.HTTP_202_ACCEPTED)

# DELETE


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def delete(request, type, idx):

    if type == "feed":
        feed = Feed.objects.get(pk=idx)
        feed.delete()
        return Response("????????? ?????????????????????.", status=status.HTTP_202_ACCEPTED)

    elif type == "comment":
        comment = Comment.objects.get(pk=idx)
        comment.delete()
        return Response("????????? ?????????????????????.", status=status.HTTP_202_ACCEPTED)

    elif type == "cocomment":
        comment = Cocomment.objects.get(pk=idx)
        comment.delete()
        return Response("???????????? ?????????????????????.", status=status.HTTP_202_ACCEPTED)


# LOAD
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def home_load(request):
    # Model?????? data get
    try:
        feeds = Feed.objects.all().order_by('-id')
    except Feed.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Serializer ??? ?????? response ??????
    if request.method == "GET":

        # ???????????????

        # ?????? ????????????
        page = request.GET.get('page')  # ?????????
        # ???????????????
        paginator = Paginator(feeds, 3)  # ???????????? 3?????? ????????????
        page_obj = paginator.get_page(page)
        # print(page_obj.end_index())# ??? ?????? ??????

        # ???????????????
        serializer = FeedSerializer(page_obj, many=True)
        for data in serializer.data:
            try:
                
                for d in data['feed_comment']:
                    print(d['author_id'])
                profile = Profile.objects.get(author_id = data['author_id'])
                profile_sz = UserProfileSerializer(profile)

                data.update({'profile_image':profile_sz.data['profile_image'],
                             'nickname':profile_sz.data['nickname']})
            
            except:#?????? ????????? superuser??? ???????????? ????????? ????????? ????????? ?????????????????? try catch??????
                data.update({'profile_image':None,
                             'nickname':None})

            try:
                liked = Like.objects.get(feed_id=data['id'], author_id=request.user.id)
                data.update({'feed_liked':1})
            except:
                pass

            like_count = Like.objects.filter(feed_id = data['id']).count()
            data.update({'feed_like_count':like_count})
            
            if data['username'] == request.user.username:
                data.update({'is_author': 1})

        return Response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def detail_load(request, idx):

    # Model?????? data get
    try:

        feed = Feed.objects.get(pk=idx)

    except Feed.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Serializer ??? ?????? response ??????
    if request.method == "GET":

        serializer = FeedSerializer(feed)

        for comment in serializer.data['feed_comment']:
            try:
                profile = Profile.objects.get(author_id = comment['author_id'])
                profile_sz = UserProfileSerializer(profile)
                comment.update({'profile_image':profile_sz.data['profile_image'],
                                'nickname':profile_sz.data['nickname']})
            except:#?????? ????????? superuser??? ???????????? ????????? ????????? ????????? ?????????????????? try catch??????
                comment.update({'profile_image':None,
                                'nickname':None})
            
            try:
                liked = Like.objects.get(comment_id=comment['id'], author_id=request.user.id)
                comment.update({'comment_liked': 1})
            except:
                pass
            
            comment_like_count = Like.objects.filter(comment_id=comment['id']).count()
            comment.update({'comment_like_count':comment_like_count})

            if comment['username'] == request.user.username:
                comment.update({'is_author': 1})

            for cocomment in comment['cocomment']:
                if cocomment['username'] == request.user.username:
                    cocomment.update({'is_author': 1})

        return_dict = {}
        return_dict.update(serializer.data)

        try:
            profile = Profile.objects.get(author_id = request.user.id)
            profile_sz = UserProfileSerializer(profile)
            return_dict.update({'profile_image':profile_sz.data['profile_image'],
                            'nickname':profile_sz.data['nickname']})
        
        except:#?????? ????????? superuser??? ???????????? ????????? ????????? ????????? ?????????????????? try catch??????
            return_dict.update({'profile_image':None,
                                'nickname':None})

        if serializer.data['username'] == request.user.username:
            return_dict.update({'is_author': 1})

        try:
            liked = Like.objects.get(feed_id=idx, author_id=request.user.id)
            return_dict.update({'feed_liked': 1})
        
        except:
            pass

        like_count = Like.objects.filter(feed_id = idx).count()
        return_dict.update({'feed_like_count':like_count})

        return Response(return_dict)

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_like(request, type, idx):
    profile_list = []
    return_dict = {}

    if type =='feed':
        like = Like.objects.filter(feed_id = idx)

        for l in like:
            profile = Profile.objects.get(author_id = l.author_id)
            profile_sz = UserProfileSerializer(profile)
            profile_list.append({'profile_image':profile_sz.data['profile_image'],
                                 'nickname':profile_sz.data['nickname'],
                                 'author_id':l.author_id})

        return_dict['Like_list'] = profile_list

        return Response(return_dict)
    
    elif type =='comment':
        like = Like.objects.filter(comment_id = idx)

        for l in like:
            profile = Profile.objects.get(author_id = l.author_id)
            profile_sz = UserProfileSerializer(profile)
            profile_list.append({'profile_image':profile_sz.data['profile_image'],
                                 'nickname':profile_sz.data['nickname'],
                                 'author_id':l.author_id})

        return_dict['Like_list'] = profile_list

        return Response(return_dict)