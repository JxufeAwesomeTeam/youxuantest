from django.shortcuts import render

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import list_route
from rest_framework.response import Response

from apps.login.jwt import verify_token
from apps.login.models import User
from apps.book.models import Book

from .serializer import HistorySerializer
from .models import History
# Create your views here.
class BookHistoryViewSet(ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    '''
    当用户点击一个链接 即说明他访问过这个对象（书或者其他）
    前端设置在点击连接时发送一个POST请求 其中包含访问的类型id和对象作为该类型的id
    '''
    @list_route()
    def history(self,request):
        user_id = verify_token(request)
        book_id = request.GET.get('bid',None)
        if user_id and book_id:
            user = User.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)
            newHistory = History.objects.create(user=user,book=book)
            newHistory.save()
            return Response(data='OJBK!',status=200)
        elif not book_id:
            return Response(data='参数错误！',status=404)
        elif not user_id:
            return Response(data='请重新登录！',status=404)








