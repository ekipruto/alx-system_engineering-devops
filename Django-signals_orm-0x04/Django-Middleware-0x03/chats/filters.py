import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter by sender's email (via FK relationship)
    sender_email = django_filters.CharFilter(
        field_name="sender__email", lookup_expr="icontains"
    )

    # Filter by sent_at timestamp
    start_date = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="gte"
    )
    end_date = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="lte"
    )

    class Meta:
        model = Message
        fields = ["sender_email", "start_date", "end_date"]