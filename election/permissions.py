from account.permissions import IsInspector, IsSupervisor
from .models import Election


class CanInspectorConfirmVote(IsInspector):
    message = 'User must be inspector of this election and election status must be pending for inspector'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.inspector.user and obj.status == Election.ElectionStatus.PENDING_FOR_INSPECTOR


class CanSupervisorConfirmVote(IsSupervisor):
    message = 'User must be supervisor of this election and election status must be pending for supervisor'

    def has_object_permission(self, request, view, obj):
        return request.user == obj.supervisor.user and obj.status == Election.ElectionStatus.PENDING_FOR_SUPERVISOR
