import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import user_management.settings.base
from .managers import CustomUserManager


AUTH_PROVIDERS = {'google': 'google', 'email': 'email'}

class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(verbose_name=("Username"), max_length=225,
                                unique=True)
    first_name = models.CharField(verbose_name=("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=("Last Name"), max_length=50)
    email = models.EmailField(verbose_name=("Email Address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_signed = models.BooleanField(verbose_name=_("User Signed"),
                                    default=False)

    available = models.BooleanField(default=True, null=True)
    favorite_players = models.ManyToManyField("User", verbose_name=_("Favorite Players"), blank=True, related_name="favorites")
    created = models.DateTimeField(auto_now_add=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    ## the name of user of the user , that a user needs to identify
    USERNAME_FIELD="email"
    # it requires a user to submit a username
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username

