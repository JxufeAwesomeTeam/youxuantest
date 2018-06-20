from rest_framework import serializers
from .models import Share

from apps.login.serializer import UserSerializer
from apps.book.serializer import ISBNSerializer
class BookShareSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = ISBNSerializer(read_only=True)
    class Meta:
        model = Share
        fields = ('id','book','share_text','user','share_time','like')
        depth = 1