from rest_framework import permissions
from .models import Commitment

class IsCommitmentOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            commitment_id = request.resolver_match.kwargs.get('pk')
            commitment = Commitment.objects.get(id=commitment_id)
            return commitment.user == request.user
        except:
            return False
