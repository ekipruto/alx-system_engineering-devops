from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Message

@login_required
def delete_user(request):
    request.user.delete()
    return redirect('login')

def inbox(request):
    unread_messages = Message.unread.for_user(request.user)
    return unread_messages


def threaded_conversation(request):
    messages = (Message.objects.filter(parent_message__isnull=True) \
        .filter(sender=request.user, parent_message__isnull=True)
        .select_related('sender', 'receiver') \
        .prefetch_related('replies')
    )
    return messages

def get_thread(message):
    thread = []
    for reply in message.replies.all():
        thread.append(reply)
        thread.extend(get_thread(reply))
    return thread
