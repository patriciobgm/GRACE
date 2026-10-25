from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include,path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
from apps.accounts.views import MeView,LogoutView,UserViewSet
from apps.organization.views import OfficeViewSet
from apps.core.views import AttachmentViewSet,ActivityHistoryViewSet,SystemSettingViewSet
from apps.core.dashboard import DashboardView
from apps.governance.views import StrategicObjectiveViewSet,GovernanceKPIViewSet,GovernanceDecisionViewSet
from apps.risks.views import RiskCategoryViewSet,RiskViewSet,RiskMitigationViewSet,RiskIndicatorViewSet
from apps.compliance.views import ComplianceObligationViewSet,ComplianceEvidenceViewSet,ComplianceFindingViewSet,CorrectiveActionViewSet
from apps.monitoring.views import MonitoringAlertViewSet,RunMonitoringViewSet
from apps.ai_support.views import AIAnalysisViewSet
from apps.notifications.views import NotificationViewSet
from apps.audit.views import AuditLogViewSet
from apps.reports.views import ReportListView,ReportExportView

router=DefaultRouter()
for prefix,view,base in [
 ("users",UserViewSet,"users"),("offices",OfficeViewSet,"offices"),("attachments",AttachmentViewSet,"attachments"),("activity",ActivityHistoryViewSet,"activity"),("settings",SystemSettingViewSet,"settings"),
 ("governance/objectives",StrategicObjectiveViewSet,"objectives"),("governance/kpis",GovernanceKPIViewSet,"kpis"),("governance/decisions",GovernanceDecisionViewSet,"decisions"),
 ("risk-categories",RiskCategoryViewSet,"risk-categories"),("risks",RiskViewSet,"risks"),("risk-mitigations",RiskMitigationViewSet,"risk-mitigations"),("risk-indicators",RiskIndicatorViewSet,"risk-indicators"),
 ("compliance/obligations",ComplianceObligationViewSet,"obligations"),("compliance/evidence",ComplianceEvidenceViewSet,"evidence"),("compliance/findings",ComplianceFindingViewSet,"findings"),("compliance/corrective-actions",CorrectiveActionViewSet,"corrective-actions"),
 ("monitoring/alerts",MonitoringAlertViewSet,"alerts"),("monitoring/run",RunMonitoringViewSet,"monitoring-run"),("ai/analyses",AIAnalysisViewSet,"ai-analyses"),("notifications",NotificationViewSet,"notifications"),("audit",AuditLogViewSet,"audit")]: router.register(prefix,view,basename=base)

urlpatterns=[path("admin/",admin.site.urls),path("api/schema/",SpectacularAPIView.as_view(),name="schema"),path("api/docs/",SpectacularSwaggerView.as_view(url_name="schema"),name="swagger-ui"),
 path("api/v1/auth/login/",TokenObtainPairView.as_view()),path("api/v1/auth/refresh/",TokenRefreshView.as_view()),path("api/v1/auth/logout/",LogoutView.as_view()),path("api/v1/auth/me/",MeView.as_view()),
 path("api/v1/dashboard/",DashboardView.as_view()),path("api/v1/reports/",ReportListView.as_view()),path("api/v1/reports/<slug:slug>/",ReportExportView.as_view()),path("api/v1/",include(router.urls))]
if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

