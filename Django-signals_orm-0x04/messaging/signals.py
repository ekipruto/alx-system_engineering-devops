from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import Message, Notification,MessageHistory
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    When a Message is created, create a Notification for the receiver.
    """
    if not created:
        return

    if instance.sender_id == instance.receiver_id:
        return

    Notification.objects.create(
        user=instance.receiver,
        message=instance,
    )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content
        )
        instance.edited = True

