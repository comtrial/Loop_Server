from django.shortcuts import render, redirect
import json
from django.contrib.auth.models import User
from .serializers import UserCustomSerializer
from .models import UserCustom
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

# for email check
from django.conf.global_settings import SECRET_KEY
from django.views import View
from .text import message 
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.http              import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)
from django.utils.encoding          import (
    force_bytes,
    force_text
)   
from django.conf.global_settings import SECRET_KEY
import jwt
# from .text import message 
 
# Create your views here.

# user 등록
# input: {
#   username: ''
#   password: ''
# }
@api_view(["POST", ])
def signup_checkemail(request):
    User = get_user_model()
    if request.method == "POST":
        
        data = request.data
        username = data['username']
        email = data['email']
        password = data['password']
        department = data['department']
        email = data['email']
        print(department)
        # django 제공 User 객체에 user 등록 진행
        user = User.objects.create_user(
            username = username,
            email =  email,
            password =  password,
            department=department,
            is_active = False
            )

        # token = Token.objects.create(user = user)
        # user.save()

        #email check
        current_site = get_current_site(request)
        domain = current_site.domain
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = jwt.encode({'id': user.id}, SECRET_KEY,algorithm='HS256')
        message_data = message(domain, uidb64, token)


        main_title = '이메일 인증을 완료해주세요'
        mail_to = email
        email = EmailMessage(main_title, message_data, to=[mail_to])
        email.send()


        res_data = {}
        res_data['message'] = 'login success'
        #response
        return Response(res_data)


    # http method 가 post 가 아닐 경우
    else:
        #response
        return Response({ 'message': 'incorrenct method type please change method to "POST"'})


class Activate(View):
    def get(self, request, uidb64, token):
        
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserCustom.objects.get(pk=uid)
        user_dic = jwt.decode(token,algorithms='HS256')
        if user.id == user_dic['id']:
            user.is_active = True
            user.save()

            return redirect("https://w.namu.la/s/ff250ecf6b040d461d70a54825fa840816bd399369d4fbcc9e71fe21a028435757556a886cf579feff0c97d373cbe88619c0d2bce59f741e21f2668dffe7978bc834e9da9ef0c3609b4bc5b89476f166d8c98764bdc2047eaf910159f9387d8e510ce80dc6238b903ffaf01f2b30e052")
    
        return Response({'message':'email check fail...'})
        
    # except KeyError:
    #     return JsonResponse({'message':'INVALID_KEY'}, status=400)

@api_view(["POST", ])
def signup(request):
    User = get_user_model()
    if request.method == "POST":
        
        data = request.data
        username = data['username']
        email = data['email']
        password = data['password']
        department = data['department']

        # django 제공 User 객체에 user 등록 진행
        user = UserCustom.objects.get(username = username)

        # email 인증 됬을 경우
        if user.is_active:

            try:
                token = Token.objects.create(user = user)
                print(token)
                user.save()

                res_data = {}
                res_data['message'] = 'login success'
                res_data['token'] = str(token)
                res_data['isAuthorization'] = 1
                #response
                return Response(res_data)

            except:
                res_data = {}
                res_data['message'] = '이미 등록된 사용자 입니당..'
                return Response(res_data)
            
        
        # email 인증 안됨
        res_data = {}
        res_data['message'] = 'login failed'
        res_data['isAuthorization'] = 0
        #response
        return Response(res_data)
        
        


    # http method 가 post 가 아닐 경우
    else:
        #response
        return Response({ 'message': 'incorrenct method type please change method to "POST"'})