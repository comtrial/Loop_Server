from django.shortcuts import render
import json
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
# Create your views here.

# user 등록
# input: {
#   username: ''
#   password: ''
# }
@api_view(["POST", ])
def signup(request):
    if request.method == "POST":
        
        ## user signup logic
        # web 이 아니기 때문에 request.post.get()이 아닌
        # body json parsing
        # body_unicode = request.body
        # body = json.loads(body_unicode)

        # 이 방법 쓰려면 serializer 거쳐와야대
        data = request.data
        username = data['username']
        password = data['password']

        # django 제공 User 객체에 user 등록 진행
        user = User.objects.create_user(username, password)
        user.save()



        ## Response with user Token
        token = Token.objects.get(user = user).key
        res_data = {}
        res_data['message'] =  'login success'
        res_data['token'] =  token
        #response
        return Response(res_data)


    # http method 가 post 가 아닐 경우
    else:
        #response
        return Response({ 'message': 'incorrenct method type please change method to "POST"'})