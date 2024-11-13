from django.db import models
from django.db.models import ForeignKey
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField


class Restaurant(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_("სახელი")
    )
    address = models.CharField(
        max_length=100,
        verbose_name=_("მისამართი")
    )
    phone = models.CharField(
        max_length=9,
        verbose_name=_("ტელეფონის ნომერი")
    )
    cover = VersatileImageField(
        help_text=_("ატვირთეთ ფოტოსურათი"),
        blank=True,
        null=True,
        verbose_name=_("გარეკანის ფოტოსურათი")
    )
    user = ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name='restaurant',
        verbose_name=_("მომხმარებელი")
    )

    def __str__(self):
        return self.name
