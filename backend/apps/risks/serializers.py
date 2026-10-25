from django.utils import timezone
from rest_framework import serializers
from .models import RiskCategory,Risk,RiskMitigationAction,RiskIndicator
from .services import assess_risk,calculate_risk_score,determine_risk_level,update_kri_status
class RiskCategorySerializer(serializers.ModelSerializer):
    class Meta: model=RiskCategory; fields="__all__"
class RiskSerializer(serializers.ModelSerializer):
    category_name=serializers.CharField(source="category.name",read_only=True); office_name=serializers.CharField(source="office.name",read_only=True); owner_name=serializers.CharField(source="risk_owner.get_full_name",read_only=True)
    class Meta: model=Risk; fields="__all__"; read_only_fields=["inherent_risk_score","inherent_risk_level","residual_risk_score","residual_risk_level","created_by"]
    def create(self,data):
        data["inherent_risk_score"]=calculate_risk_score(data["likelihood"],data["impact"])
        data["inherent_risk_level"]=determine_risk_level(data["inherent_risk_score"])
        data["residual_risk_score"]=calculate_risk_score(data["residual_likelihood"],data["residual_impact"])
        data["residual_risk_level"]=determine_risk_level(data["residual_risk_score"])
        return Risk.objects.create(**data)
    def update(self,instance,data):
        for k,v in data.items(): setattr(instance,k,v)
        return assess_risk(instance)
class RiskMitigationSerializer(serializers.ModelSerializer):
    class Meta: model=RiskMitigationAction; fields="__all__"
    def validate(self,data):
        status=data.get("status",getattr(self.instance,"status",None)); completed=data.get("completed_at",getattr(self.instance,"completed_at",None))
        if status=="COMPLETED" and not completed: data["completed_at"]=timezone.now()
        return data
class RiskIndicatorSerializer(serializers.ModelSerializer):
    class Meta: model=RiskIndicator; fields="__all__"; read_only_fields=["status"]
    def create(self,data): return update_kri_status(RiskIndicator.objects.create(**data))
    def update(self,instance,data):
        for k,v in data.items(): setattr(instance,k,v)
        return update_kri_status(instance)

