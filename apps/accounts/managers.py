from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from apps.common.managers import GetOrNoneQuerySet


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address."))

    def validate_google_user(self, first_name, last_name, email, google_id):
        if not first_name or not last_name:
            raise ValueError(_("First name and last name are required."))

        if not google_id:
            raise ValueError(_("Google ID is required."))

        if email:
            self.email_validator(email)
        else:
            raise ValueError(_("A valid email address is required."))

    def create_user(self, first_name, last_name, email, google_id, **extra_fields):
        self.validate_google_user(first_name, last_name, email, google_id)
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            google_id=google_id,
            **extra_fields
        )
        user.set_unusable_password()  # No password used for Google login
        user.save(using=self._db)
        return user

    async def acreate_user(self, first_name, last_name, email, google_id, **extra_fields):
        self.validate_google_user(first_name, last_name, email, google_id)
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            google_id=google_id,
            **extra_fields
        )
        user.set_unusable_password()
        await user.asave(using=self._db)
        return user

    def validate_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not email:
            raise ValueError(_("Superuser must have an email address."))
        if not password:
            raise ValueError(_("Superuser must have a password."))

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        self.email_validator(email)
        return extra_fields

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields = self.validate_superuser(email, password, **extra_fields)
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    async def acreate_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields = self.validate_superuser(email, password, **extra_fields)
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        await user.asave(using=self._db)
        return user

    def get_queryset(self):
        return GetOrNoneQuerySet(self.model, using=self._db)

    def get_or_none(self, **kwargs):
        return self.get_queryset().get_or_none(**kwargs)

    async def aget_or_none(self, **kwargs):
        return await self.get_queryset().aget_or_none(**kwargs)
