# Generated by Django 5.1.2 on 2024-11-12 22:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_alter_dish_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='dish',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='restaurant.dish', verbose_name='კერძი'),
        ),
    ]