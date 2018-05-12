import django_filters
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import list_route
from rest_framework.viewsets import GenericViewSet,ReadOnlyModelViewSet
from rest_framework.mixins import RetrieveModelMixin,ListModelMixin

from .models import Book, BookType
from .serializer import BookTypeSerializer,BookSerializer


class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    #模糊匹配书名 返回一个符合的序列化Book List
    filter_fields = {
        'title': ['icontains']
    }

class BookTypeViewSet(ReadOnlyModelViewSet):
    queryset = BookType.objects.all()
    serializer_class = BookTypeSerializer


#全类热门书籍 Top 10
class HotBookViewSet(ListModelMixin,
                     GenericViewSet):
    queryset = Book.objects.all().order_by('-review')[:10]
    serializer_class = BookSerializer


