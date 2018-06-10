from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from rest_framework.viewsets import ViewSet,GenericViewSet
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework.decorators import action

from .models import User
from .forms import UserForm,RegisterForm
from .serializer import UserSerializer
from .jwt import set_token,verify_token

import json

class UserViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    '''

    用户操作 POST：注册，登录

    用户信息 GET：查询单个用户信息，返回所有用户信息

    信息修改 PUT：修改用户信息(beta)
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @csrf_exempt
    @action(methods=['post'],detail=False)
    def register(self, request):
        register_form = request.POST
        username = register_form.get('username')
        password1 = register_form.get('password1')
        password2 = register_form.get('password2')
        email = register_form.get('email')
        sex = register_form.get('sex')

        if password1 != password2:
            message = "两次输入的密码不同!"
            return HttpResponse(status=404, content={message})
        elif not password1[0].isalpha():
            message = "密码首字符应该为字母[a-z][A-Z]!"
            return HttpResponse(status=404, content={message})
        elif password1.isspace():
            message = "密码不能包含空格!"
            return HttpResponse(status=404, content={message})
        elif 6 > len(password1) > 12:
            message = "密码的长度不应该少于6位,不多于12位"
            return HttpResponse(status=404, content={message})
        elif not password1.isalnum():
            message = "包含非法字符,密码应该由字母[a-z][A-Z]与数字[0-9]组成!"
            return HttpResponse(status=404, content={message})
        else:
            same_name_user = User.objects.filter(username=username)
            if same_name_user:
                message = "用户名已被注册，请重新选择用户名!"
                return HttpResponse(status=404, content={message})

            same_email_user = User.objects.filter(email=email)
            if same_email_user:
                message = "邮箱地址已被注册，请重新选择邮箱!"
                return HttpResponse(status=404, content={message})

        new_user = User.objects.create()
        new_user.username = username
        new_user.password = password1
        new_user.email = email
        new_user.sex = sex
        new_user.save()
        return HttpResponse(status=201, content={"注册成功"})

    @csrf_exempt
    @action(methods=['post'],detail=False)
    def login(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = self.queryset.get(username=username)  # 获得user数据
        except:
            message = "用户不存在！"
            return HttpResponse(status=404, content={message})
        else:
            if user.password == password:  # 判断密码是否正确

                payload = {
                    'uid':str(user.id),
                }
                token = set_token(payload) #生成Token
                user.save()
                return HttpResponse(status=201, content={token})
            else:
                message = "密码不正确!"
                return HttpResponse(status=404, content={message})

    @csrf_exempt
    @action(methods=['put'],detail=False)
    def UpdateInfo(self,request):
        uid = verify_token(request)
        post = request.POST.dict()
        user = User.objects.get(id=uid)
        for key,value in post.items():
            if key == 'username':
                user.username = value
            elif key == 'password':
                user.password = value
            elif key == 'email':
                user.email = value
            elif key == 'sex':
                user.sex = value

            user.save()
        return HttpResponse('hello')

