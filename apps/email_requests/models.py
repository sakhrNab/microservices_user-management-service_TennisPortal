from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel


class EmailRequest(TimeStampedUUIDModel):
    name = models.CharField(_('Your name'), max_length=100)
    phone_number = models.CharField(_('Phone number'), max_length=30,
    default="+415151151")
    email = models.EmailField(_("Email"))
    subject = models.CharField(_('Subject'), max_length=30)
    message = models.TextField(_('Message'))

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Email Requests"