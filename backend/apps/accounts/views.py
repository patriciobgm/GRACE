from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from apps.core.services import record_activity
from .models import User
from .permissions import IsSystemAdministrator
from .serializers import UserSerializer

class MeView(generics.RetrieveAPIView):
    serializer_class=UserSerializer
    def get_object(self): return self.request.user

class LogoutRequestSerializer(serializers.Serializer):
    refresh=serializers.CharField()
class LogoutView(generics.GenericAPIView):
    serializer_class=LogoutRequestSerializer
    def post(self,request):
        token=request.data.get("refresh")
        if not token: return Response({"refresh":"This field is required."},status=400)
        RefreshToken(token).blacklist()
        record_activity(actor=request.user,instance=request.user,action="LOGOUT",description="User logged out",request=request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.select_related("office").all(); serializer_class=UserSerializer; permission_classes=[IsSystemAdministrator]
    filterset_fields=["role","office","is_active"]; search_fields=["username","email","first_name","last_name"]; ordering_fields=["username","email","date_joined"]
    def perform_create(self,serializer):
        obj=serializer.save(); record_activity(actor=self.request.user,instance=obj,action="USER_CREATED",description=f"Created user {obj.username}",request=self.request)
    def get_permissions(self):
        if self.action in ["list","retrieve"]: return [permissions.IsAuthenticated()]
        return [IsSystemAdministrator()]

