from json.decoder import JSONDecoder
from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import GroupImageSerializer, GroupSerializer, CrewSerializer, UserProfileSerializer
from .models import Group, Crew, GroupImage
from user_api.models import UserCustom
import json

from rest_framework import status
from rest_framework.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


from user_api.models import Profile
# Create your views here.


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def create_group(request):
    leader = request.user

    print(request.data['group_name'])
    # 그루비룸 중복 체크
    try:
        duplicate = Group.objects.get(group_name=request.data['group_name'])
        # Group 명 중복 처리
        if duplicate != None:
            return Response("이미 있는 이름입니다.", status=HTTP_409_CONFLICT)
        else:
            pass

    except:
        # MARK - make_Group logic
        group = Group(group_leader=leader,
                      group_name=request.data['group_name'], group_description=request.data['group_description'])
        group.save()

        group_sz = GroupSerializer(group)

        try:
            for image in request.FILES.getlist('image'):
                image_sz = GroupImageSerializer(data={'group': group.id, 'image': request.FILES['image']})
                if image_sz.is_valid():
                    image_sz.save()

        except:
            return Response('유효하지 않은 형식입니다.', status=status.HTTP_403_FORBIDDEN)

        return Response(group_sz.data, status=HTTP_201_CREATED)


# Create your views here.


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def create_crew(request, group_idx):
    user = request.user

    try:
        crew = UserCustom.objects.get(id=request.data['crew'])
        group = Group.objects.get(id=group_idx)

        # crew 중복되는거 처리해줘야 될 거 같은데

        crew = Crew(crew=crew, group=group)
        crew.save()

        crew_sz = CrewSerializer(crew)

        return Response(crew_sz.data, status=status.HTTP_201_CREATED)
    except:
        return Response('유효하지 않은 형식입니다.', status=status.HTTP_403_FORBIDDEN)

    # # Group 명 중복 처리
    # if crew_sz.is_valid():
    #     crew_sz.save()
    #     return Response(crew_sz.data, status=HTTP_201_CREATED)

    # else:
    #     return Response('유효하지 않은 형식입니다.', status = status.HTTP_403_FORBIDDEN)


# Create your views here.
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def read_group(request, group_idx):

    group = Group.objects.get(id=group_idx)

    group_sz = GroupSerializer(group)
    res_dict = group_sz.data
    
    # for use profile_image
    for data in res_dict['crew']:
        print(data)
        try:
            profile = Profile.objects.get(author_id = data['crew'])
            print(profile.nickname)
            profile_sz = UserProfileSerializer(profile)
            print(profile_sz.data['profile_image'])
            data.update({'profile_image':profile_sz.data['profile_image'],
                             'nickname':profile_sz.data['nickname']})
        except:
            print('sdf')
            data.update({'profile_image':None,
                             'nickname':None})
    # 그룹장이면
    if group.group_leader.id == request.user.id:
        # 출력을 안하면 오류발생
        # print("group_sz.data", group_sz.data)
        res_dict = json.JSONDecoder().decode(
            json.JSONEncoder().encode(group_sz.__dict__['_data']))
        res_dict['is_author'] = '1'

    return Response(res_dict, status=HTTP_201_CREATED)


# Create your views here.
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def read_all_groups(request):

    try:
        groups = Group.objects.all()
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        group_sz = GroupSerializer(groups, many=True)
        print(group_sz.data)

    return Response(group_sz.data, status=HTTP_201_CREATED)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def group_profile_update(request, idx):
    group = Group.objects.get(id=idx)
    if group.group_leader.id == request.user.id:
        try:
            print('드루와~~')
            group = Group.objects.get(id=idx)
            print('드루와~~1')
            # group_img = GroupImage.objects.get(image=idx)
            print('드루와~~2')

            group.group_name = request.data['group_name']
            print('드루와~~3')
            group.group_description = request.data['group_description']

            print('드루와~~4')
            # group_img.profile_image = request.data['image']
            print('드루와~~5')

            group.save()
            print('드루와~~')
            return_dict = {
                'Update Completed'
            }
            return Response(return_dict)
        except Group.DoesNotExist:
            return Response('Request is not valid.', status=status.HTTP_404_NOT_FOUND)
    else:
        return_dict = {
            'message': ['No permission to modify.']
        }
        return Response(return_dict, status=status.HTTP_401_UNAUTHORIZED)
