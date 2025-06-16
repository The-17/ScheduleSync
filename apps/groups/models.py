from django.db import models
from apps.common.models import BaseModel
from apps.common.managers import GetOrNoneManager
from apps.accounts.models import User
from django.db import models
from autoslug import AutoSlugField


class Group(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, through='GroupMembership', related_name='joined_groups')
    is_active = models.BooleanField(default=True)
    objects = GetOrNoneManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'SyncGroup'
        verbose_name_plural = 'SyncGroups'


class GroupMembership(BaseModel):

    ROLE_CHOICES = [
        ("member", 'Member'),
        ("admin", 'Admin'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)
    objects = GetOrNoneManager()
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.full_name} - {self.group.name} ({self.role})"
