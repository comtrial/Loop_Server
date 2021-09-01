from django.http import response
from rest_framework.decorators import parser_classes
from rest_framework.views import APIView
from django.shortcuts import render, redirect
import json
from django.contrib.auth.models import User
from .serializers import UserCustomSerializer, ProfileSerializer, Customizing_imgs_Serializer, CustomizingSerializer
from feed_api.serializer import FeedSerializer
from .models import Customizing, Customizing_imgs, UserCustom, Profile
from feed_api.models import Feed
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
        current_site = get_current_site(request)
        domain = current_site.domain
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        # token = jwt.encode({'id': user.id}, SECRET_KEY,algorithm='HS256').decode('utf-8')# ubuntu환경
        token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
        message_data = message(domain, uidb64, token)

        main_title = '이메일 인증을 완료해주세요'
        mail_to = email
        email = EmailMessage(main_title, message_data, to=[mail_to])
        email.send()

        res_data = {}
        res_data['message'] = 'login success'
        # response
        return Response(res_data)

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
        username = data['username']
        # email = data['email']
        # password = data['password']
        # department = data['department']

        # django 제공 User 객체에 user 등록 진행
        user = UserCustom.objects.get(username=username)

        # profile information 추가
        # email 인증 됬을 경우
        if user.is_active:
            try:
                token = Token.objects.create(user=user)
                user.save()
                profile = Profile(author=user)
                data = {
                    'nickname': data['nickname'],
                    'grade': data['grade'],
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

            except:
                res_data = {}
                res_data['message'] = '이미 등록된 사용자 입니당..'
                return Response(res_data)

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
            'grade': profile_sz.data['grade']
        }

        feed_list = FeedSerializer(feeds, many=True)
        customizing_list = CustomizingSerializer(customizings, many=True)

        custom_list = customizing_list.data
        
        return_dict = {
            'profile_info': profile_info,
            # 'feed_list': feed_list.data,
            'custom_list': custom_list
        }

        # 본인 프로필 확인
        if str(request.user.id) == idx:
            return_dict = {
                'profile_info': profile_info,
                'feed_list': feed_list.data,
                'custom_list': custom_list,
                'is_author': '1'
            }

        return Response(return_dict)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def profile_update(request, prof_type, idx):
    if str(request.user.id) == idx:
        try:
            if prof_type == 'profile_info':
                try:
                    profile = Profile.objects.get(author=idx)
                    profile.profile_image = request.data['image']
                    profile.nickname = request.data['nickname']
                    profile.real_name = request.data['real_name']
                    profile.class_num = request.data['class_num']
                    profile.grade = request.data['grade']
                    # feed.content = request.data['content']
                    profile.save()
                    return_dict = {
                        'Update Completed'
                    }
                    return Response(return_dict)
                except Profile.DoesNotExist:
                    return Response('Request is not valid.', status=status.HTTP_404_NOT_FOUND)

            elif prof_type == 'customizing':

                cum_val = 0

                customizing = Customizing.objects.filter(author_id=idx)
                customizing.delete()

                customizing = Customizing_imgs.objects.filter(author_id=idx)
                customizing.delete()

                try:
                    param_data = request.data['customizing_data']
                    req_list = json.JSONDecoder().decode(param_data)
                    return_list = []
                    for line in req_list:
                        customizing_model = Customizing(author=request.user)
                        customizing_sz = CustomizingSerializer(customizing_model, data={
                            'type': line['type'],
                            'contents': line['contents'],
                            'seq_id': line['id']
                        })
#############################################################################################################################
                        if line['type'] == 'title' or line['type'] == 'content':
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

                            print('text updated')

#############################################################################################################################
                        elif line['type'] == 'image':
                            if customizing_sz.is_valid():
                                customizing_sz.save()
                            else:
                                return Response('유효하지 않은 형식입니다.', status=status.HTTP_403_FORBIDDEN)

                            try:

                                start_num = cum_val
                                end_num = start_num + line['contents']
                                cum_val = end_num

                                pointed_list = request.FILES.getlist(
                                    'image')[start_num:end_num]

                                image_list = []
                                for image in pointed_list:
                                    try:
                                        custom_model = Customizing_imgs(
                                            author=request.user)
                                    except:
                                        return Response('없는 사용자입니다.', status=status.HTTP_404_NOT_FOUND)
                                    customizing_imgs_sz = Customizing_imgs_Serializer(
                                        custom_model, data={'customizing': customizing_sz.data['id'], 'image': image})
                                    if customizing_imgs_sz.is_valid():
                                        customizing_imgs_sz.save()
                                        print("customizing_imgs_sz:",
                                              customizing_imgs_sz)
                                        image_list.append(
                                            customizing_imgs_sz.data['image'])
                                    else:
                                        print("데이터가 저장되지 않았습니다.")

                                return_list.append(
                                    {
                                        "id": customizing_sz.data['seq_id'],
                                        "type": customizing_sz.data['type'],
                                        "contents": image_list,
                                    }
                                )

                            except:
                                return Response('유효하지 않은 image 형식입니다.', status=status.HTTP_403_FORBIDDEN)
#############################################################################################################################
                        elif line['type'] == 'feed':
                            try:
                                if customizing_sz.is_valid():
                                    customizing_sz.save()
                                else:
                                    return Response('유효하지 않은 형식입니다.', status=status.HTTP_403_FORBIDDEN)

                                feed = Feed.objects.get(
                                    id=customizing_sz.data['contents'])
                                serializer = FeedSerializer(feed)
                                print(serializer.data)
                                # return_dict = {}
                                # return_dict.update(serializer.data)

                            except Feed.DoesNotExist:
                                return Response(status=status.HTTP_404_NOT_FOUND)
                            print('feed updated')

                            return_list.append(
                                {
                                    "id": customizing_sz.data['seq_id'],
                                    "type": customizing_sz.data['type'],
                                    "contents": serializer.data,
                                }
                            )
                    print("return_list:", return_list)
                    # return_dict = {}
                    # for one_line in return_list:
                    #     return_dict.update(one_line)
                    # return_dict = {
                    #     return_list
                    # }

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
