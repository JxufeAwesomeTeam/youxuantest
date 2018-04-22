from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,filters
from rest_framework.decorators import detail_route,list_route

from apps.login.models import User
from apps.login import forms
from apps.login.serializer import UserSerializer

class DefaultsMixin(object):

    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class UserViewSet(DefaultsMixin,viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        register_from = forms.RegisterForm(request.POST)
        message = '请检查填写的内容'
        if register_from.is_valid():
            username = register_from.cleaned_data['username']
            password1 = register_from.cleaned_data['password1']
            password2 = register_from.cleaned_data['password2']
            email = register_from.cleaned_data['email']
            sex = register_from.cleaned_data['sex']

            if password1 != password2:
                message = "两次输入的密码不同!"
                return HttpResponse(status=404, content={"message1": message})
            elif not password1[0].isalpha():
                message = "密码首字符应该为字母[a-z][A-Z]!"
                return HttpResponse(status=404, content={"message2": message})
            elif password1.isspace():
                message = "密码不能包含空格!"
                return HttpResponse(status=404, content={"message3": message})
            elif 6 > len(password1) > 12:
                message = "密码的长度不应该少于6位,不多于12位"
                return HttpResponse(status=404, content={"message4": message})
            elif not password1.isalnum():
                message = "包含非法字符,密码应该由字母[a-z][A-Z]与数字[0-9]组成!"
                return HttpResponse(status=404, content={"message5": message})
            else:
                same_name_user = User.objects.filter(username=username)
                if same_name_user:
                    message = "用户名已被注册，请重新选择用户名!"
                    return HttpResponse(status=404, content={"message6": message})

                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = "邮箱地址已被注册，请重新选择邮箱!"
                    return HttpResponse(status=404, content={"message7": message})

            new_user = User.objects.create()
            new_user.username = username
            new_user.password = password1
            new_user.email = email
            new_user.sex = sex
            new_user.save()
            return HttpResponse(status=201, content={"message8": "注册成功"})
        return HttpResponse(status=404, content={"message9": message})

    @csrf_exempt
    @list_route(methods=['post'])
    def login(self,request):
        if request.method == "POST":
            login_form = forms.UserForm(request.POST)  # 初始化表单
            message = "请检查填写的内容!"
            if login_form.is_valid():  # 判断数据格式合法
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                try:
                    user = User.objects.get(username=username)  # 获得user数据
                    if user.password == password:  # 判断密码是否正确
                        request.session['is_login'] = True  # 设置session  保持登录状态
                        request.session['user_id'] = user.id  # 用户id
                        request.session['user_name'] = username  # 用户名
                        message = "登录成功!"
                        return HttpResponse(status=201, content={"message1": message})
                    else:
                        message = "密码不正确!"
                except:
                    message = "用户不存在！"
            return HttpResponse(status=404, content={"message2": message})
        return HttpResponse(status=404, content={"message3": "请登录"})




