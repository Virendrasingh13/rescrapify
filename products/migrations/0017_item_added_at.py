# Generated by Django 5.0.2 on 2024-03-17 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_item_likes_item_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='added_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
