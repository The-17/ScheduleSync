from .models import Group, GroupMembership
from asgiref.sync import sync_to_async


class GroupMixin:
    async def __filter__(self, filters):
        queryset = await sync_to_async(lambda: list(Group.objects.filter(**filters)),thread_sensitive=True)()
        return queryset
    
    async def get_groups(self, user_id, group_filter):

        if group_filter.lower() == "created":
            return await self.__filter__({"created_by": user_id})
        
        elif group_filter.lower() == "joined":
            group_ids = await sync_to_async(lambda: list(GroupMembership.objects.filter(user_id=user_id).values_list("group_id", flat=True)),thread_sensitive=True)()
            filter = {"id__in": group_ids}
            return await self.__filter__(filter)

    async def get_group(self, group_slug):
        return await Group.objects.select_related("created_by").prefetch_related("members").aget_or_none(slug=group_slug)

