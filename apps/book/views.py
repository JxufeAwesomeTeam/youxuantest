from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_list_or_404,get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet,ReadOnlyModelViewSet
from rest_framework.mixins import RetrieveModelMixin,ListModelMixin

from .models import Book, BookType,ISBNBook
from .serializer import BookTypeSerializer,BookSerializer,ISBNSerializer


class BookViewSet(ReadOnlyModelViewSet):
    '''

    书籍操作：GET 获取全部书籍/通过id获取单本书籍

    HotByType: GET 通过btype获取该类的前10评论数书籍

    '''
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    #模糊匹配书名 返回一个符合的序列化Book List
    filter_fields = {
        'title': ['icontains']
    }

    #通过类别获取评价数前10书籍
    @action(methods=['get'],detail=False)
    def HotByType(self,request):
        btype = request.GET.get('btype')
        if btype:
            bookType = get_object_or_404(BookType,typename=btype)
            queryset = Book.objects.filter(typename=bookType).order_by('-review')[:10]
            serializer = BookSerializer(instance=queryset,many=True)
            return Response(data=serializer.data,status=200)
        else:
            return Response('未找到该类型的书籍商品！',status=404)

class BookTypeViewSet(ReadOnlyModelViewSet):
    queryset = BookType.objects.all()
    serializer_class = BookTypeSerializer

class ISBNBookViewSet(ReadOnlyModelViewSet):

    queryset = ISBNBook.objects.annotate(Count('Books')).filter(Books__count=3)
    serializer_class = ISBNSerializer

    filter_fields = {
        'title': ['icontains']
    }

    @action(methods=['get'],detail=False)
    def ByType(self,request):
        btype = request.GET.get('btype')
        if btype:
            bookType = get_object_or_404(BookType, typename=btype)
            queryset = ISBNBook.objects.filter(typename=bookType)
            serializer = self.serializer_class(instance=queryset, many=True)
            return Response(data=serializer.data, status=200)
        else:
            return Response('未找到该类型的书籍商品！', status=400)