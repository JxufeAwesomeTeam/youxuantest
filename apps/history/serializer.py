from rest_framework import serializers
from .models import History

class HistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = History
        fields = ('id','user','book','visit_time')
        depth = 1

