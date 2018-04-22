from rest_framework import serializers, validators
from .models import BookType,Book


class BookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookType
        fields = ('typename',)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
       # fields = ('id', 'title','typename','price', 'url', 'loc', 'photo','owner')
        fields ='__all__'
        depth = 1
