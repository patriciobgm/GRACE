from django.utils import timezone
from rest_framework import decorators,response,viewsets
from .models import Notification
from .serializers import NotificationSerializer
class NotificationViewSet(viewsets.ModelViewSet):
    queryset=Notification.objects.none()
    serializer_class=NotificationSerializer; http_method_names=["get","patch","head","options"]; filterset_fields=["is_read","type"]
    def get_queryset(self):
        if getattr(self,"swagger_fake_view",False) or not self.request.user.is_authenticated: return Notification.objects.none()
        return Notification.objects.filter(user=self.request.user)
    @decorators.action(detail=False,methods=["post"],url_path="mark-all-read")
    def mark_all_read(self,request):
        count=self.get_queryset().filter(is_read=False).update(is_read=True,read_at=timezone.now()); return response.Response({"updated":count})

