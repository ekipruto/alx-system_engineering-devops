from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    edited=models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='edited_messages',
        # set to null to keep history even if user is deleted
        on_delete=models.SET_NULL
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message(from={self.sender}, to={self.receiver}, at={self.timestamp})"


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    # optionally: type or text preview
    preview = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        # set a short preview if not provided
        if not self.preview and self.message and self.message.content:
            self.preview = (self.message.content[:200]).replace("\n", " ")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notification(user={self.user}, message_id={self.message_id}, read={self.read})"
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='histories', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit history for message {self.message_id}"

