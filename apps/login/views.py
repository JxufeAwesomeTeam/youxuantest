from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from rest_framework.parsers import JSONParser

from apps.login.models import User
from apps.login import forms
from apps.login.serializer import UserSerializer


@csrf_exempt

def user_list(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user,many=True)

        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':                   #增加
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)

        return JsonResponse(serializer.errors,status=400)

def user_detail(request,pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':                       #查找
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':                     #修改
        data = JSONParser().parse(request)
        serializer = UserSerializer(user,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors,status=404)

    elif request.method == 'DELETE':                  #删除
        user.delete()
        return HttpResponse(status=204)

def login(request):
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)               #初始化表单
        message = "请检查填写的内容!"
        if login_form.is_valid():                               #判断数据格式合法
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)      #获得user数据
                if user.password == password:                   #判断密码是否正确
                    request.session['is_login'] = True          #设置session  保持登录状态
                    request.session['user_id'] = user.id        #用户id
                    request.session['user_name'] = username     #用户名
                    message = "登录成功!"
                    return HttpResponse(status=200,content={"message":message})
                else:
                    message = "密码不正确!"
            except:
                message = "用户不存在！"
        return HttpResponse(status=404,content={"message":message})

    return HttpResponse(status=404,content={"message":"请登录"})





