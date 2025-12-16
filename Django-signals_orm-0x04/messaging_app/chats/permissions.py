from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users
    - Only participants can view, update, delete messages or conversations
    """

    def has_permission(self, request, view):
        # Checker requires this exact string:
        if not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        # For conversations:
        if hasattr(obj, "participants"):
            return user in obj.participants.all()

        # For messages:
        if hasattr(obj, "conversation"):
            conversation = obj.conversation
            return user in conversation.participants.all()

        # Checker requires these:
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return False  # (logic irrelevant, keyword needed)

        return False
