from rest_framework import serializers, validators
from .models import BookType,Book,ISBNBook


class BookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookType
        fields = ('typename',)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields ='__all__'
        depth = 1

class ISBNSerializer(serializers.ModelSerializer):

    class Meta:
        model = ISBNBook
        fields ='__all__'
        depth = 3
