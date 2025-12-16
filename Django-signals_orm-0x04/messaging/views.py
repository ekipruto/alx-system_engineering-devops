from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Message

@login_required
def delete_user(request):
    request.user.delete()
    return redirect('login')

def threaded_conversation(request):
    messages = Message.objects.filter(parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies')

    return messages

def get_thread(message):
    thread = []
    for reply in message.replies.all():
        thread.append(reply)
        thread.extend(get_thread(reply))
    return thread
