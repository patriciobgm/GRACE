from rest_framework import serializers
from .models import AIAnalysis
class AIAnalysisSerializer(serializers.ModelSerializer):
    requested_by_name=serializers.CharField(source="requested_by.get_full_name",read_only=True); reviewed_by_name=serializers.CharField(source="reviewed_by.get_full_name",read_only=True)
    class Meta: model=AIAnalysis; fields="__all__"; read_only_fields=[f.name for f in AIAnalysis._meta.fields]
class GenerateAnalysisSerializer(serializers.Serializer):
    analysis_type=serializers.ChoiceField(choices=AIAnalysis.Type.choices)
    entity_id=serializers.UUIDField(required=False)
    def validate(self,data):
        if data["analysis_type"]!="EXECUTIVE_BRIEF" and not data.get("entity_id"): raise serializers.ValidationError({"entity_id":"Required for entity analysis."})
        return data
class ReviewAnalysisSerializer(serializers.Serializer):
    status=serializers.ChoiceField(choices=["ACCEPTED","ACCEPTED_WITH_MODIFICATION","REJECTED"])
    comments=serializers.CharField(required=False,allow_blank=True)
    final_management_note=serializers.CharField(required=False,allow_blank=True)

