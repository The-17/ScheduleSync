from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from autoslug import AutoSlugField
from .managers import CustomUserManager
import uuid


def slugify_two_fields(self):
    return f"{self.first_name}-{self.last_name}"

AUTH_PROVIDERS = [
        ('google', 'Google'),
    ]

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(_('Email Address'), unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.URLField(null=True, blank=True)
    username = AutoSlugField(
        _("Username"), populate_from=slugify_two_fields, unique=True, always_update=True
    )
    auth_provider = models.CharField(max_length=20, choices=AUTH_PROVIDERS, default="google")
    provider_user_id = models.CharField(max_length=255, null=True, blank=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
