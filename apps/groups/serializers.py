from adrf.serializers import Serializer as AsyncSerializer
from .models import GroupMembership
from asgiref.sync import sync_to_async
from rest_framework import serializers


class CreateGroupSerializer(AsyncSerializer):
    name = serializers.CharField()
    description = serializers.CharField()


class GroupsSerializer(serializers.Serializer):
    name = serializers.CharField()
    slug = serializers.CharField()

class GroupDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    slug = serializers.CharField()
    created_by = serializers.SerializerMethodField()
    admins = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        return obj.created_by.full_name
    
    def get_members(self, obj):
        members = obj.members.all()
        return [{"id":member.id, "full_name":member.full_name} for member in members]
    
    def get_admins(self, obj):
        return self.context.get("admins", [])
    

class AssignAdminSerializer(serializers.Serializer):
    member_id = serializers.UUIDField()
    group_slug = serializers.CharField()