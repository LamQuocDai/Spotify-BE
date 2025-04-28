from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from apps.users.models import User
from .models import Chat
from .serializers import ChatSerializer
from rest_framework.permissions import IsAuthenticated

class ConversationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        user2_list = Chat.objects.filter(user1=current_user).values_list('user2', flat=True).distinct()
        user1_list = Chat.objects.filter(user2=current_user).values_list('user1', flat=True).distinct()
        all_users = set(user2_list) | set(user1_list)
        all_users.discard(current_user.id)
        conversations = User.objects.filter(id__in=all_users).values('id', 'username')
        return Response(conversations)

class MessageList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, other_user_id):
        current_user = request.user
        other_user = User.objects.get(id=other_user_id)
        messages = Chat.objects.filter(
            Q(user1=current_user, user2=other_user) | Q(user1=other_user, user2=current_user)
        ).order_by('created_at')
        serializer = ChatSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, other_user_id):
        current_user = request.user
        other_user = User.objects.get(id=other_user_id)
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            if current_user.id < other_user.id:
                user1 = current_user
                user2 = other_user
            else:
                user1 = other_user
                user2 = current_user
            chat = Chat.objects.create(
                user1=user1,
                user2=user2,
                message=serializer.validated_data['message']
            )
            return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)