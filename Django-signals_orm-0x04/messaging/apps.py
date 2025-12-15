from django.apps import AppConfig

class MessagingConfig(AppConfig):
    name = 'messaging'
    verbose_name = "Messaging"

    def ready(self):
        # import signals to register them
        from . import signals  # noqa: F401
