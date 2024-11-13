from django.db import models
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

    def __str__(self):
        return self.name


class Menu(models.Model):
    dish = models.ManyToManyField(
        "Dish",
        related_name='menus',
        verbose_name=_("კერძი"),
    )
    restaurant = models.ForeignKey(
        "Restaurant",
        verbose_name=_("რესტორანი"),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
