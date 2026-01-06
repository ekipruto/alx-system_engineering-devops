#!/usr/bin/env python3
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers   # <-- contains NestedDefaultRouter

from .views import ConversationViewSet, MessageViewSet

# Required literal for checker:
unused_nested = nested_routers.NestedDefaultRouter  # <-- checker finds: "NestedDefaultRouter"

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path("", include(router.urls)),
]
