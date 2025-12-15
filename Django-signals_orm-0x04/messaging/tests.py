# messaging/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class MessageNotificationTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='pass')
        self.user2 = User.objects.create_user(username='bob', password='pass')

    def test_notification_created_on_message_create(self):
        msg = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello Bob")
        # Expect one notification for user2
        notifications = Notification.objects.filter(user=self.user2, message=msg)
        self.assertEqual(notifications.count(), 1)
        notif = notifications.first()
        self.assertFalse(notif.read)
        self.assertIn("Hello Bob", notif.preview)

    def test_no_notification_on_edit(self):
        # ensure that updating (not creating) doesn't create another notification
        msg = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello")
        Notification.objects.filter(user=self.user2, message=msg).delete()  # ensure clean
        msg.content = "Edited"
        msg.save()
        self.assertEqual(Notification.objects.filter(user=self.user2, message=msg).count(), 0)
