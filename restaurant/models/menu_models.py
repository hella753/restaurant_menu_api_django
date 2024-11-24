from django.db import models
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField


class Category(models.Model):
    name = models.CharField(
        max_length=40,
        null=True,
        verbose_name=_("სახელი")
    )
    cover = VersatileImageField(
        help_text=_("ატვირთეთ ფოტოსურათი"),
        blank=True,
        null=True,
        verbose_name=_("გარეკანის ფოტოსურათი")
    )
    restaurant = models.ForeignKey(
        "Restaurant",
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name=_("რესტორანი")
    )

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(
        max_length=40,
        null=True,
        verbose_name=_("სახელი")
    )
    parent = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("ზეკატეგორია"),
        related_name="children"
    )
    cover = VersatileImageField(
        help_text=_("ატვირთეთ ფოტოსურათი"),
        blank=True,
        null=True,
        verbose_name=_("გარეკანის ფოტოსურათი")
    )

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(
        max_length=40,
        null=True,
        verbose_name=_("სახელი")
    )
    image = VersatileImageField(
        help_text=_("ატვირთეთ ფოტოსურათი"),
        blank=True,
        null=True,
        verbose_name=_("კერძის ფოტოსურათი")
    )
    price = models.FloatField(
        verbose_name=_("ფასი")
    )
    category = models.ForeignKey(
        "Subcategory",
        on_delete=models.CASCADE,
        related_name='dishes',
        verbose_name=_("კატეგორია")
    )
    ingredients = models.ManyToManyField(
        "Ingredient",
        verbose_name=_("ინგრედიენტები"),
        blank=True
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_("სახელი")
    )

    def __str__(self):
        return self.name
