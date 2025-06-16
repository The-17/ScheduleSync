from adrf.views import APIView
from apps.common.response import CustomResponse
from .serializers import (
    GroupsSerializer,
    CreateGroupSerializer,
    GroupDetailSerializer,
    AssignAdminSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from asgiref.sync import sync_to_async
from .models import Group, GroupMembership  
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .mixins import GroupMixin
from .permissions import IsGroupAdmin

tags = ["Group"]

class GroupListCreateAPIView(APIView, GroupMixin):
    serializer_class = GroupsSerializer
    post_serializer = CreateGroupSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
            tags = tags,
            summary = "Retreive user's groups",
            description = "This endpoint retrieves the groups a user is admin or member of",
            parameters = [
                OpenApiParameter(
                    name="group_filter",
                    description = "Filter groups by type, defaults to created - groups the user created",
                    type=str,
                    enum=["created", "joined"],
                    default="created",
                    required=False
                )
            ]
    )
    async def get(self, request):
        group_filter = request.query_params.get("group_filter", "created")
        groups = await self.get_groups(request.user.id, group_filter)

        serializers = self.serializer_class(groups, many=True)
        return CustomResponse.success(message="Groups retreived successfully", data=serializers.data)

    @extend_schema(
        tags = tags,
        summary = "Create a group",
        description = "This endpoint creates a group",
        responses=CreateGroupSerializer,
        request=CreateGroupSerializer
    )
    async def post(self, request):
        serializer = self.post_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        group = await Group.objects.acreate(
            created_by=request.user,
            name=serializer.validated_data["name"],
            description=serializer.validated_data["description"]
        )

        await GroupMembership.objects.acreate(
            user=request.user,
            group=group,
            role="admin"
        )

        serializer = self.serializer_class(group)
        return CustomResponse.success(message="Group created successfully", data=serializer.data, status_code=201)


class GroupDetailAPIView(APIView, GroupMixin):
    serializer_class = GroupDetailSerializer
    patch_serializer = CreateGroupSerializer

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsAuthenticated(), IsGroupAdmin()]
        return [AllowAny()]
    
    @extend_schema(
        tags=tags,
        summary="Get group details",
        description="""
        This endpoint retreives the details of a group
        """
    )
    async def get(self, request, group_slug):
        group = await self.get_group(group_slug)
        if not group:
            return CustomResponse.error(message="Group not found", status_code=404)
        
        admins_qs = await sync_to_async(lambda: list(GroupMembership.objects.select_related("user").filter(group=group, role="admin", active=True)),thread_sensitive=True)()
        admins = [{"id": admin.user.id, "admin":admin.user.full_name} for admin in admins_qs]

        serializer = self.serializer_class(group, context={"admins":admins})
        return CustomResponse.success(message="Group retreived successfully", data=serializer.data)

    async def patch(self, request, group_slug):
        group = await self.get_group(group_slug)
        if not group:
            return CustomResponse.error(message="Group not found", status_code=404)

        for permission in self.get_permissions():
            if not await sync_to_async(permission.has_object_permission)(request, self, group):
                return CustomResponse.error(message="Permission denied", status_code=403)
            
        
        serializer = self.patch_serializer(group, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return CustomResponse.success(message="Group updated successfully", data=serializer.data)


class JoinGroupAPIView(APIView, GroupMixin):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=tags,
        summary="Join a group",
        description="""
        This endpoint adds a user to a group
        """
    )
    async def post(self, request, group_slug):
        group = await self.get_group(group_slug=group_slug)

        if not group:
            return CustomResponse.error(message="Group not found", status_code=404)
        if not group.is_active:
            return CustomResponse.error(message="Group is inactive", status_code=400)
        
        # Check if the user is already an active member
        is_active_member = await GroupMembership.objects.aget_or_none(user=request.user, group=group, active=True)
        if is_active_member:
            return CustomResponse.error(message="You are already a member of this group", status_code=400)
        
        # Check if the user is an inactive member, if yes, simply update active to true
        is_inactive_member = await GroupMembership.objects.aget_or_none(user=request.user, group=group, active=False)
        if is_inactive_member:
            is_inactive_member.active = True
            await is_inactive_member.asave()
            return CustomResponse.success(message="Joined group successfully", status_code=201)

        await GroupMembership.objects.acreate(user=request.user, group=group, role="member")
        return CustomResponse.success(message="Joined group successfully", status_code=201)


class LeaveGroupAPIView(APIView, GroupMixin):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=tags,
        summary="Leave a group",
        description="""
        This endpoint removes a user from a group
        """
    )
    async def delete(self, request, group_slug):
        group = await self.get_group(group_slug=group_slug)

        if not group:
            return CustomResponse.error(message="Group not found", status_code=404)
        
        is_active_member = await GroupMembership.objects.aget_or_none(user=request.user, group=group, active=True)
        if not is_active_member:
            return CustomResponse.error(message="You are not a member of this group", status_code=400)

        is_active_member.active = False
        await is_active_member.asave()
        return CustomResponse.success(message="Left group successfully", status_code=200)


class RemoveUserFromGroupAPIView(APIView, GroupMixin):
    permission_classes = [IsAuthenticated, IsGroupAdmin]

    @extend_schema(
        tags=tags,
        summary="Remove from group",
        description="""
        This endpoint allows a group admin to remove a user from a group
        """
    )
    async def delete(self, request, group_slug, member_id):
        group = await self.get_group(group_slug=group_slug)
        if not group:
            return CustomResponse.error(message="Group not found", status_code=404)

        member = await GroupMembership.objects.aget_or_none(user_id=member_id, group=group, active=True)
        if not member:
            return CustomResponse.error(message="Member not found", status_code=404)
        
        member.active = False
        await member.asave()
        return CustomResponse.success(message="Removed user from group successfully", status_code=200)


class AssignAdminAPIView(APIView, GroupMixin):
    serializer_class = AssignAdminSerializer
    permission_classes = [IsAuthenticated, IsGroupAdmin]

    async def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        group_slug = serializer.validated_data["group"]
        group = await self.get_group(slug=group_slug)
        if not group:
            return CustomResponse.error(message="Group not found", status_code=404)

        member_id = serializer.validated_data["member_id"]
        member = await GroupMembership.objects.aget_or_none(user_id=member_id, group=group, active=True)
        if not member:
            return CustomResponse.error(message="Member not found", status_code=404)

        member.role = "admin"
        await member.asave()

        return CustomResponse.success(message="Assigned admin successfully")


