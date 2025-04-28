from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'message', 'created_at', 'updated_at', 'user1', 'user2']
        read_only_fields = ['user1', 'user2', 'created_at', 'updated_at']