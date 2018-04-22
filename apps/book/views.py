import django_filters

from .models import Book, BookType
from .serializer import *
from rest_framework import viewsets,filters
from django_filters.rest_framework import DjangoFilterBackend




class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_fields = {
        'title': ['icontains']
    }


class BookTypeViewSet(viewsets.ModelViewSet):
    queryset = BookType.objects.all()
    serializer_class = BookTypeSerializer

