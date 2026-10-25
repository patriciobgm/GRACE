from rest_framework import decorators,response,status,viewsets
from apps.accounts.permissions import CanReviewAI
from apps.compliance.models import ComplianceObligation
from apps.risks.models import Risk
from .models import AIAnalysis
from .serializers import AIAnalysisSerializer,GenerateAnalysisSerializer,ReviewAnalysisSerializer
from .services import generate_analysis,review_analysis
class AIAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=AIAnalysis.objects.select_related("requested_by","reviewed_by"); serializer_class=AIAnalysisSerializer
    filterset_fields=["analysis_type","human_review_status","requested_by"]; ordering_fields=["requested_at","reviewed_at"]
    @decorators.action(detail=False,methods=["post"],url_path="generate")
    def generate(self,request):
        serializer=GenerateAnalysisSerializer(data=request.data); serializer.is_valid(raise_exception=True); data=serializer.validated_data; entity=None
        if data["analysis_type"]=="RISK": entity=Risk.objects.get(pk=data["entity_id"])
        elif data["analysis_type"]=="COMPLIANCE": entity=ComplianceObligation.objects.get(pk=data["entity_id"])
        result=generate_analysis(user=request.user,analysis_type=data["analysis_type"],entity=entity,request=request)
        return response.Response(AIAnalysisSerializer(result).data,status=status.HTTP_201_CREATED)
    @decorators.action(detail=True,methods=["post"],permission_classes=[CanReviewAI])
    def review(self,request,pk=None):
        serializer=ReviewAnalysisSerializer(data=request.data); serializer.is_valid(raise_exception=True)
        try: obj=review_analysis(analysis=self.get_object(),reviewer=request.user,request=request,**serializer.validated_data)
        except ValueError as exc: return response.Response({"detail":str(exc)},status=400)
        return response.Response(AIAnalysisSerializer(obj).data)

