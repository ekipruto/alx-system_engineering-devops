from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Message

@login_required
def delete_user(request):
    request.user.delete()
    return redirect('login')

from django.contrib.auth.decorators import login_required
from .models import Message

def inbox(request):
    unread_messages = (
        Message.unread.unread_for_user(request.user)
        .only('id', 'content', 'timestamp', 'sender')
    )
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


@cache_page(60)
def message_list(request):
    messages = Message.objects.all().values('id', 'content', 'timestamp')
    return JsonResponse(list(messages), safe=False)
