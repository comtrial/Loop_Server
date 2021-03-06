from group_api.models import Group
from django.http import response
from rest_framework.decorators import parser_classes
from rest_framework.views import APIView
from django.shortcuts import render, redirect
import json
from django.contrib.auth.models import User
from .serializers import UserCustomSerializer, ProfileSerializer, Customizing_imgs_Serializer, CustomizingSerializer
from feed_api.serializer import FeedSerializer
from group_api.serializers import CrewSerializer, GroupSerializer
from feed_api.serializer import HashTagSerializer
from .models import Customizing, Customizing_imgs, UserCustom, Profile
from feed_api.models import Feed
from group_api.models import Group, Crew
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

# for email check
from django.conf.global_settings import SECRET_KEY
from django.views import View
from .text import message
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)
from django.utils.encoding import (
    force_bytes,
    force_text
)
from django.conf.global_settings import SECRET_KEY
from .department import DEPARTMENT
import jwt
import time

@api_view(["POST", ])
def signup_checkemail(request):
    User = get_user_model()
    if request.method == "POST":

        data = request.data
        email = data['email']
        username = email
        password = data['password']
        department = data['department']

        # django 제공 User 객체에 user 등록 진행
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            department=department,
            is_active=False
        )

        # token = Token.objects.create(user = user)
        # user.save()

        # email check
        user_pk = user.id
        current_site = get_current_site(request)
        domain = current_site.domain
        uidb64 = urlsafe_base64_encode(force_bytes(user_pk))
        # token = jwt.encode({'id': user.id}, SECRET_KEY,algorithm='HS256').decode('utf-8')# ubuntu환경
        token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
        message_data = message(domain, uidb64, token)

        main_title = '이메일 인증을 완료해주세요'
        mail_to = email
        email = EmailMessage(main_title, message_data, to=[mail_to])
        email.send()

        for i in range(6):
            time.sleep(30)
            user = User.objects.get(pk=user_pk)

            if user.is_active:
                res_data = {}
                res_data['message'] = 'login success'

                return Response(res_data)
        
        user.delete()

        return Response({'message': '인증이 만료되었습니다.'})

    # http method 가 post 가 아닐 경우
    else:
        # response
        return Response({'message': 'incorrenct method type please change method to "POST"'})


class Activate(View):
    def get(self, request, uidb64, token):

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserCustom.objects.get(pk=uid)
        user_dic = jwt.decode(token, algorithms='HS256')
        if user.id == user_dic['id']:
            user.is_active = True
            user.save()

            return redirect("https://w.namu.la/s/ff250ecf6b040d461d70a54825fa840816bd399369d4fbcc9e71fe21a028435757556a886cf579feff0c97d373cbe88619c0d2bce59f741e21f2668dffe7978bc834e9da9ef0c3609b4bc5b89476f166d8c98764bdc2047eaf910159f9387d8e510ce80dc6238b903ffaf01f2b30e052")

        return Response({'message': 'email check fail...'})

    # except KeyError:
    #     return JsonResponse({'message':'INVALID_KEY'}, status=400)


@api_view(["POST", ])
def signup(request):
    User = get_user_model()
    if request.method == "POST":

        data = request.data
        username = data['email']
        # email = data['email']
        # password = data['password']
        # department = data['department']

        # django 제공 User 객체에 user 등록 진행
        user = UserCustom.objects.get(username=username)

        # profile information 추가
        # email 인증 됬을 경우
        if user.is_active:
            # try:
            token = Token.objects.create(user=user)
            user.save()
            profile = Profile(author=user)
            data = {
                'nickname': data['nickname'],
                'class_num': data['class_num'],
                'real_name': data['real_name']
            }
            profile_sz = ProfileSerializer(profile, data=data)
            if profile_sz.is_valid():
                profile_sz.save()
            else:
                return Response('profile information is not invalid', status=status.HTTP_403_FORBIDDEN)

            res_data = {}
            res_data['message'] = 'login success'
            res_data['token'] = str(token)
            res_data['isAuthorization'] = 1
            # response
            return Response(res_data)

            # except:
            #     res_data = {}
            #     res_data['message'] = '이미 등록된 사용자 입니당..'
            #     return Response(res_data)

        # email 인증 안됨
        res_data = {}
        res_data['message'] = 'login failed'
        res_data['isAuthorization'] = 0
        # response
        return Response(res_data)

    # http method 가 post 가 아닐 경우
    else:
        # response
        return Response({'message': 'incorrenct method type please change method to "POST"'})


@api_view(["POST", ])
def login(request):

    if request.method == "POST":

        user = authenticate(
            username=request.data['username'], password=request.data['password'])
        if user is not None:
            token = Token.objects.get(user=user)
            return Response({
                "Token": token.key,
                "user_id": str(token.user_id)
            })
        else:
            return Response(status=401)

    # http method 가 post 가 아닐 경우
    else:
        # response
        return Response({'message': 'incorrenct method type please change method to "POST"'})


@api_view(["GET", ])
def get_list(request):
    if request.method == 'GET':
        return Response(DEPARTMENT)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def profile_load(request, idx):
    # request.user.
    try:
        profile = Profile.objects.get(author=idx)

    except Profile.DoesNotExist:
        return Response('해당 유저의 profile이 유효하지않습니다.', status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        feeds = Feed.objects.filter(author_id=idx)
        customizings = Customizing.objects.filter(author_id=idx)
        profile_sz = ProfileSerializer(profile)

        profile_info = {
            # 'profile_image' : request.FILES.get('image'),
            'profile_image': profile_sz.data['profile_image'],
            'nickname': profile_sz.data['nickname'],
            'real_name': profile_sz.data['real_name'],
            'class_num': profile_sz.data['class_num'],
            'introduction': profile_sz.data['introduction']
        }

        feed_list = FeedSerializer(feeds, many=True)
        customizing_list = CustomizingSerializer(customizings, many=True)

        custom_list = customizing_list.data

        for one_custom in custom_list:
            if one_custom["type"] == "feed":
                feed_num = int(one_custom["contents"])
                corres_feed = Feed.objects.get(id=feed_num)
                feed = FeedSerializer(corres_feed)
                one_custom["contents"] = feed.data

        crews = Crew.objects.filter(crew=idx)
        crew_sz = CrewSerializer(crews, many=True)

        group_list = []
        for i in crew_sz.data:
            group = Group.objects.get(pk=i['group'])
            group_sz = GroupSerializer(group)
            group_info = group_sz.data
            del group_info['crew']
            group_list.append(group_info)
        # group_list = ''.join(group_list)
        # group_list = ''.join(map(str, group_list))

        return_dict = {
            'profile_info': profile_info,
            # 'feed_list': feed_list.data,
            'group_list': group_list,
            'custom_list': custom_list
        }

        # 본인 프로필 확인
        if str(request.user.id) == idx:
            return_dict = {
                'profile_info': profile_info,
                'feed_list': feed_list.data,
                'group_list': group_list,
                'custom_list': custom_list,
                'is_author': '1'
            }

        return Response(return_dict)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def profile_update(request, prof_type, idx):
    if str(request.user.id) == idx:

        try:
            if prof_type == 'profile_info_picture':
                try:
                    profile = Profile.objects.get(author=idx)
                    profile.profile_image = request.data['image']
                    profile.save()

                    profile = Profile.objects.get(author=idx)
                    profile_sz = ProfileSerializer(profile)
                    
                    return_dict = {
                        "profile_image": profile_sz.data['profile_image']
                    }
                    return Response(return_dict)
                except Profile.DoesNotExist:
                    return Response('Profile data is not valid', status=status.HTTP_404_NOT_FOUND)

            elif prof_type == 'profile_info_hashtag':
            
                profile = Profile.objects.get(author=idx)
                for tag in request.data['hashtag'].split('#'):
                    if tag != '':
                        tag_sz = HashTagSerializer(
                            data={'profile': profile.id, 'tag': tag})
                        try:
                            tag_sz.is_valid()
                            tag_sz.save()
                        except:
                            return Response('유효하지 않은 형식입니다.', status=status.HTTP_403_FORBIDDEN)
                return Response(tag_sz.data)


            elif prof_type == 'profile_info_context':
                try:
                    profile = Profile.objects.get(author=idx)

                    profile_sz = ProfileSerializer(profile, data = {
                        'nickname': request.data['nickname'],
                        'real_name': request.data['real_name'],
                        'class_num': request.data['class_num'],
                        'introduction': request.data['introduction']
                    })
                    profile_sz.is_valid()
                    profile_sz.save()
                    
                    print('Update Completed')
                    return Response(profile_sz.data)
                except Profile.DoesNotExist:
                    return Response('Profile data is not valid', status=status.HTTP_404_NOT_FOUND)

            elif prof_type == 'customizing':

                # cum_val = 0

                customizing = Customizing.objects.filter(author_id=idx)
                customizing.delete()

                customizing = Customizing_imgs.objects.filter(author_id=idx)
                customizing.delete()

                try:
                    param_data = request.data['customizing_data']
                    req_list = json.JSONDecoder().decode(param_data)
                    return_list = []
                    i = 0
                    for line in req_list:
#############################################################################################################################
                        if line['type'] == 'title' or line['type'] == 'content':
                            customizing_model = Customizing(author=request.user)
                            customizing_sz = CustomizingSerializer(customizing_model, data={
                                'type': line['type'],
                                'contents': line['contents'],
                                'seq_id': line['id']
                        })
                            if customizing_sz.is_valid():
                                customizing_sz.save()

                            else:
                                return Response('유효하지 않은 형식입니다.', status=status.HTTP_403_FORBIDDEN)

                            return_list.append(
                                {
                                    "id": customizing_sz.data['seq_id'],
                                    "type": customizing_sz.data['type'],
                                    "contents": customizing_sz.data['contents'],
                                }
                            )

#############################################################################################################################
                        elif line['type'] == 'imageURL':
                            customizing_model = Customizing(author=request.user)
                            customizing_sz = CustomizingSerializer(customizing_model, data={
                                'type': line['type'],
                                'contents': line['contents'],
                                'seq_id': line['id']
                        })
                            if customizing_sz.is_valid():
                                customizing_sz.save()
                            else:
                                return Response('유효하지 않은 형식입니다.', status=status.HTTP_403_FORBIDDEN)

                            try:
                                return_list.append(
                                    {
                                        "id": customizing_sz.data['seq_id'],
                                        "type": customizing_sz.data['type'],
                                        "contents": customizing_sz.data['contents'],
                                    }
                                )

                            except:
                                return Response('Error', status=status.HTTP_403_FORBIDDEN)
#############################################################################################################################
                        elif line['type'] == 'imageFILE':
                            customizing_model = Customizing(author=request.user)
                            customizing_sz = CustomizingSerializer(customizing_model, data={
                                'type': line['type'],
                                'contents': line['contents'],
                                'seq_id': line['id']
                        })
                            if customizing_sz.is_valid():
                                customizing_sz.save()
                            else:
                                return Response('유효하지 않은 형식입니다.', status=status.HTTP_403_FORBIDDEN)

                            req_image_data = request.FILES.getlist('image')[i]
                            i = i + 1
                            try:
                                custom_model = Customizing_imgs(author=request.user)
                            except:
                                return Response('없는 사용자입니다.', status=status.HTTP_404_NOT_FOUND)
                            customizing_imgs_sz = Customizing_imgs_Serializer(
                                custom_model, data={'customizing': customizing_sz.data['id'], 'image': req_image_data})
                            try:
                                if customizing_imgs_sz.is_valid():
                                    customizing_imgs_sz.save()
                                else:
                                    print("데이터가 저장되지 않았습니다.")
                                return_list.append(
                                    {
                                        "id": customizing_sz.data['seq_id'],
                                        "type": customizing_sz.data['type'],
                                        "contents": customizing_imgs_sz.data['image'],
                                    }
                                )
                            except:
                                return Response('유효하지 않은 image 형식입니다.??', status=status.HTTP_403_FORBIDDEN)
#############################################################################################################################
                        elif line['type'] == 'feed':
                            customizing_model = Customizing(author=request.user)
                            customizing_sz = CustomizingSerializer(customizing_model, data={
                                'type': line['type'],
                                'contents': line['contents'],
                                'seq_id': line['id']
                        })
                            try:
                                if customizing_sz.is_valid():
                                    customizing_sz.save()
                                else:
                                    return Response('유효하지 않은 형식입니다.', status=status.HTTP_403_FORBIDDEN)

                                feed = Feed.objects.get(
                                    id=customizing_sz.data['contents'])
                                serializer = FeedSerializer(feed)
                                # return_dict = {}
                                # return_dict.update(serializer.data)

                            except Feed.DoesNotExist:
                                return Response(status=status.HTTP_404_NOT_FOUND)

                            return_list.append(
                                {
                                    "id": customizing_sz.data['seq_id'],
                                    "type": customizing_sz.data['type'],
                                    "contents": serializer.data,
                                }
                            )
                    return Response(return_list)

                except Profile.DoesNotExist:
                    return Response('Request is not valid.', status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response('Request is not valid.', status=status.HTTP_404_NOT_FOUND)
    else:
        return_dict = {
            'message': ['No permission to modify.']
        }
        return Response(return_dict, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST', ])
# @permission_classes((IsAuthenticated,))
# def profile_customizing(request, type, idx):

#     if type == 'feed':
#         feed = Feed.objects.get(pk=idx)
#         feed.title = request.data['title']
#         feed.content = request.data['content']
#         feed.save()

#         tag = HashTag.objects.filter(feed_id = feed.id)
#         tag.delete()

#         for tag in request.data['hashtag'].split('#'):
#             if tag != '':
#                 tag_sz = HashTagSerializer(data = {'feed':feed.id, 'tag':tag})
#                 if tag_sz.is_valid():
#                     tag_sz.save()

#     if type == 'comment':
#         comment = Comment.objects.get(pk = idx)
#         comment.content = request.data['content']
#         comment.save()


# @parser_classes((MultiPartParser, ))
# class UploadFileAndJson(APIView):

#     def post(self, request, format=None):
#         print('여기까지는 들어온다')
#         file_data = request.FILES["image"]
#         print('이미지 다음')
#         # info_data = request.data["0"]
#         print('json 다음')
#         res_data = {
#             "file_data": file_data
#             # "info_data": info_data
#         }
#         print("res_data:", res_data)

#         return response(file_data)
#         return response(res_data)
