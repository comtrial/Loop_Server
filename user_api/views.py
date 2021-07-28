from django.shortcuts import render
import json
from django.contrib.auth.models import User
from .serializers import UserCustomSerializer
from .models import UserCustom
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
# Create your views here.

# user 등록
# input: {
#   username: ''
#   password: ''
# }
@api_view(["POST", ])
def signup(request):
    User = get_user_model()
    if request.method == "POST":
        
        data = request.data
        username = data['username']
        email = data['email']
        password = data['password']
        department = data['department']
        print(department)
        # django 제공 User 객체에 user 등록 진행
        user = User.objects.create_user(username, email, password, department=department)

        token = Token.objects.create(user = user)
        user.save()

        res_data = {}
        res_data['message'] = 'login success'
        res_data['token'] = token.key
        #response
        return Response(res_data)


    # http method 가 post 가 아닐 경우
    else:
        #response
        return Response({ 'message': 'incorrenct method type please change method to "POST"'})