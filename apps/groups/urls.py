from django.urls import path
from .views import (
    GroupListCreateAPIView,
    GroupDetailAPIView,
    JoinGroupAPIView,
    LeaveGroupAPIView,
    RemoveUserFromGroupAPIView,
    AssignAdminAPIView
)

urlpatterns = [
    path("groups/", GroupListCreateAPIView.as_view(), name="group-list-create"),
    path("groups/<str:group_slug>/", GroupDetailAPIView.as_view(), name="group-detail"),
    path("groups/<str:group_slug>/join/", JoinGroupAPIView.as_view(), name="join-group"),
    path("groups/<str:group_slug>/leave/", LeaveGroupAPIView.as_view(), name="leave-group"),

    # Admin endpoints
    path("groups/<str:group_slug>/remove/<uuid:member_id>/", RemoveUserFromGroupAPIView.as_view(), name="remove-user-from-group"),
    path("groups/asign-admin/", AssignAdminAPIView.as_view(), name="assign-admin"),
]