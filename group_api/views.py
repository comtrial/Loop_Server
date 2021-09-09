from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import GroupSerializer, GroupImageSerializer,CrewSerializer
from .models import  Group, Crew
from user_api.models import UserCustom

from rest_framework import status
from rest_framework.status import HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

# Create your views here.
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def create_group(request):
    leader = request.user

    print(request.data['group_name'])
    # 그루비룸 중복 체크
    try:
        duplicate = Group.objects.get(group_name = request.data['group_name'])
        # Group 명 중복 처리
        if duplicate != None:
            return Response("이미 있는 이름입니다.", status=HTTP_409_CONFLICT)
        else:
            pass

    except:
        #MARK - make_Group logic
        group = Group(group_leader = leader, group_name = request.data['group_name'], group_description = request.data['group_description'])
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
        crew = UserCustom.objects.get(id = request.data['crew'])
        group = Group.objects.get(id = group_idx)

        # crew 중복되는거 처리해줘야 될 거 같은데

        crew= Crew(crew = crew, group = group)
        crew.save()

        crew_sz = CrewSerializer(crew)
    
        return Response(crew_sz.data, status=status.HTTP_201_CREATED)
    except:
        return Response('유효하지 않은 형식입니다.', status = status.HTTP_403_FORBIDDEN)

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

    group = Group.objects.get(id = group_idx)
    group_sz = GroupSerializer(group)


    return Response(group_sz.data, status=HTTP_201_CREATED)
    
 