from rest_framework import serializers
from .models import History

from apps.book.serializer import ISBNSerializer

class HistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    book = ISBNSerializer(read_only=True)
    class Meta:
        model = History
        fields = ('id','user','book','visit_time')
