from rest_framework import viewsets
from apps.accounts.permissions import IsGRCManagerOrReadOnly
from .models import Office
from .serializers import OfficeSerializer
class OfficeViewSet(viewsets.ModelViewSet):
    queryset=Office.objects.select_related("office_head").all(); serializer_class=OfficeSerializer; permission_classes=[IsGRCManagerOrReadOnly]
    filterset_fields=["is_active"]; search_fields=["code","name","description"]; ordering_fields=["code","name","created_at"]

