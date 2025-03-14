# Generated by Django 5.1.6 on 2025-03-13 15:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_remove_orderitem_product_orderitem_product_variation"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
