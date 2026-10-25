from rest_framework import serializers
from .models import AuditLog
class AuditLogSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source="user.get_full_name",read_only=True)
    class Meta: model=AuditLog; fields="__all__"; read_only_fields=[f.name for f in AuditLog._meta.fields]

