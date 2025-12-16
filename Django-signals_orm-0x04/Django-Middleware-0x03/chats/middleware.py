# chats/middleware.py
import logging
from django.http import HttpResponseForbidden, JsonResponse
from datetime import datetime
import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger to write to requests.log
        logging.basicConfig(
            filename="requests.log",
            level=logging.INFO,
            format="%(message)s"
        )

    def __call__(self, request):
        # Get user info (Anonymous if not logged in)
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log the request details
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Continue processing the request
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to chat endpoints
    outside the allowed time window (6PM - 9PM).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server time (24-hour format)
        current_hour = datetime.now().hour

        # Allowed window: 18 (6PM) <= hour < 21 (9PM)
        if not (18 <= current_hour < 21):
            return HttpResponseForbidden(
                "Access to chat is restricted outside 6PM - 9PM."
            )

        # Continue normal request flow
        response = self.get_response(request)
        return response

import time
from django.http import JsonResponse

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track requests per IP: {ip: [timestamps]}
        self.ip_requests = {}
        self.limit = 5          # max messages
        self.time_window = 60   # seconds (1 minute)

    def __call__(self, request):
        # Only enforce on POST requests (chat messages)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()

            # Initialize list if IP not tracked yet
            if ip not in self.ip_requests:
                self.ip_requests[ip] = []

            # Filter out timestamps older than 1 minute
            self.ip_requests[ip] = [
                ts for ts in self.ip_requests[ip] if now - ts < self.time_window
            ]

            # Check if limit exceeded
            if len(self.ip_requests[ip]) >= self.limit:
                return JsonResponse(
                    {"error": "Message limit exceeded. Try again later."},
                    status=429
                )

            # Record this request timestamp
            self.ip_requests[ip].append(now)

        # Continue normal request flow
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Helper to extract client IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

from django.http import JsonResponse

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only enforce role checks if user is authenticated
        if request.user.is_authenticated:
            # Assuming 'role' is a field on your User model
            user_role = getattr(request.user, "role", None)

            # Allow only admin or moderator
            if user_role not in ["admin", "moderator"]:
                return JsonResponse(
                    {"error": "Forbidden: insufficient permissions"},
                    status=403
                )

        # Continue normal flow
        response = self.get_response(request)
        return response