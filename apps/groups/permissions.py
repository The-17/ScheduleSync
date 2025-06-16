from rest_framework.permissions import BasePermission
from .models import Group, GroupMembership


class IsGroupAdmin(BasePermission):
    async def has_permission(self, request, view):
        group_slug = view.kwargs.get("group_slug")
        if not group_slug or not request.user.is_authenticated:
            return False

        try:
            group = await Group.objects.aget(slug=group_slug)
        except Group.DoesNotExist:
            return False

        membership = await GroupMembership.objects.aget_or_none(user=request.user, group=group, active=True)
        return membership and membership.role == "admin"
    
