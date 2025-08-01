# Generated by Django 5.2.4 on 2025-08-01 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
        ("pedidos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pedido",
            name="cliente",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pedidos",
                to="accounts.cliente",
                verbose_name="Cliente",
            ),
        ),
        migrations.DeleteModel(
            name="Cliente",
        ),
    ]
