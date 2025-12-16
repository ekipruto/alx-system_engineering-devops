from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import IsParticipantOfConversation
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .pagination import MessagePagination
from .filters import MessageFilter
from  django_filters.rest_framework import DjangoFilterBackend


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    lookup_field = "conversation_id"

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants__user_id=user.user_id)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by("-sent_at")
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "message_id"

    def get_queryset(self):
        user = self.request.user
        conversation_id = self.kwargs.get("conversation_id")

        return Message.objects.filter(
            conversation__conversation_id=conversation_id,
            conversation__participants__user_id=user.user_id
        )

    def create(self, request, *args, **kwargs):
        conversation_id = kwargs.get("conversation_id")
        conversation = Conversation.objects.get(conversation_id=conversation_id)

        if not conversation.participants.filter(user_id=request.user.user_id).exists():
            return Response(
                {"detail": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            sender=request.user,
            conversation=conversation
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
