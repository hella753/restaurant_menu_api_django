# Generated by Django 5.1.2 on 2024-11-12 22:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_remove_category_level_remove_category_lft_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='restaurant.subcategory', verbose_name='კატეგორია'),
        ),
    ]
