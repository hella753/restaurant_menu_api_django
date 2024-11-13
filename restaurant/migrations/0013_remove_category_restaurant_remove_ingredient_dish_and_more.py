# Generated by Django 5.1.2 on 2024-11-13 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0012_restaurant_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='dish',
        ),
        migrations.AddField(
            model_name='category',
            name='restaurant',
            field=models.ManyToManyField(related_name='categories', to='restaurant.restaurant', verbose_name='რესტორანი'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='dish',
            field=models.ManyToManyField(null=True, related_name='ingredients', to='restaurant.dish', verbose_name='კერძი'),
        ),
    ]
