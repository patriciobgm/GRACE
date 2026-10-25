from rest_framework.permissions import BasePermission, SAFE_METHODS

ADMIN_ROLES = {"SYSTEM_ADMIN", "GRC_ADMIN"}
GRC_ROLES = {"GRC_ADMIN", "EXECUTIVE", "COMPLIANCE_OFFICER", "RISK_OWNER", "AUDITOR"}

class IsSystemAdministrator(BasePermission):
    def has_permission(self, request, view): return request.user.is_authenticated and request.user.role == "SYSTEM_ADMIN"

class IsGRCAdministrator(BasePermission):
    def has_permission(self, request, view): return request.user.is_authenticated and request.user.role == "GRC_ADMIN"

class IsGRCManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view): return request.user.is_authenticated and (request.method in SAFE_METHODS or request.user.role in ADMIN_ROLES)

class CanReviewAI(BasePermission):
    def has_permission(self, request, view): return request.user.is_authenticated and request.user.role in {"EXECUTIVE", "GRC_ADMIN"}

