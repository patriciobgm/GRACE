from pathlib import Path
from django.conf import settings
from rest_framework import serializers
from .models import ActivityHistory, Attachment, SystemSetting

ALLOWED_EXTENSIONS={".pdf",".doc",".docx",".xls",".xlsx",".csv",".png",".jpg",".jpeg"}
ALLOWED_TYPES={"application/pdf","application/msword","application/vnd.openxmlformats-officedocument.wordprocessingml.document","application/vnd.ms-excel","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet","text/csv","image/png","image/jpeg"}
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta: model=Attachment; fields=["id","file","original_filename","content_type","file_size","uploaded_by","uploaded_at","description"]; read_only_fields=["original_filename","content_type","file_size","uploaded_by","uploaded_at"]
    def validate_file(self,file):
        if file.size > settings.MAX_UPLOAD_SIZE: raise serializers.ValidationError("File exceeds the upload limit.")
        if Path(file.name).suffix.lower() not in ALLOWED_EXTENSIONS: raise serializers.ValidationError("File extension is not allowed.")
        if file.content_type not in ALLOWED_TYPES: raise serializers.ValidationError("File type is not allowed.")
        return file
    def create(self,data):
        file=data["file"]; return Attachment.objects.create(**data,original_filename=Path(file.name).name,content_type=file.content_type,file_size=file.size,uploaded_by=self.context["request"].user)
class ActivityHistorySerializer(serializers.ModelSerializer):
    actor_name=serializers.CharField(source="actor.get_full_name",read_only=True)
    class Meta: model=ActivityHistory; fields="__all__"
class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta: model=SystemSetting; fields="__all__"

