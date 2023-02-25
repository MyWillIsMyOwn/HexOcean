# Generated by Django 4.1.7 on 2023-02-21 17:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0017_alter_image_binary_image_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="tier",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="accounts",
                to="main.tier",
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="link_date_expiration",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 2, 21, 17, 22, 32, 549930)
            ),
        ),
    ]