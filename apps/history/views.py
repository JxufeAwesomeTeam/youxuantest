from django.shortcuts import render

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
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
    当用户点击一个链接 即说明他访问过这个书籍商品
    前端设置在点击连接时发送一个GET请求 参数为书籍商品的bid 请求头需要带Token
    
    若之前已经有记录则更新访问时间，否则新建记录
    
    若未带上参数bid 则直接返回该用户全部数据
    
    若未带Token 则提示404
    '''
    @action(methods=['get'],detail=False)
    def history(self,request):
        user_id = verify_token(request)

        if user_id:
            user = User.objects.get(id=user_id)
            #查看是否有参数bid，若有则添加记录，没有则直接返回个人全部记录
            try:
                book_id = request.GET.get('bid', None)
                book = Book.objects.get(id=book_id)
            except:
                pass
            else:
                # 若已经浏览过则删除原记录
                History.objects.filter(user=user, book=book).delete()
                # 新建记录
                newHistory = History.objects.create(user=user, book=book)
                newHistory.save()

            #返回该用户的浏览记录
            listHistory = History.objects.filter(user=user)
            serializer = self.serializer_class(listHistory,many=True)
            return Response(data=serializer.data,status=200)
        else:
            return Response(data='请重新登录！',status=404)








