# Generated by Django 5.1.2 on 2024-11-14 12:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0014_remove_category_restaurant_remove_ingredient_dish_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='dish',
        ),
        migrations.AddField(
            model_name='dish',
            name='ingredients',
            field=models.ManyToManyField(related_name='ing_dishes', to='restaurant.ingredient', verbose_name='ინგრედიენტები'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant', to=settings.AUTH_USER_MODEL, verbose_name='მომხმარებელი'),
        ),
    ]
