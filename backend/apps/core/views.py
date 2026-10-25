from rest_framework import mixins, viewsets
from apps.accounts.permissions import IsGRCManagerOrReadOnly, IsSystemAdministrator
from .models import ActivityHistory, Attachment, SystemSetting
from .serializers import ActivityHistorySerializer, AttachmentSerializer, SystemSettingSerializer
class AttachmentViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset=Attachment.objects.all(); serializer_class=AttachmentSerializer
class ActivityHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=ActivityHistorySerializer; filterset_fields=["entity_type","entity_id","action"]
    def get_queryset(self): return ActivityHistory.objects.select_related("actor").all()
class SystemSettingViewSet(viewsets.ModelViewSet):
    queryset=SystemSetting.objects.all(); serializer_class=SystemSettingSerializer; permission_classes=[IsSystemAdministrator]

