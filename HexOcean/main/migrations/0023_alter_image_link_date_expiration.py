# Generated by Django 4.1.7 on 2023-02-24 18:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0022_alter_account_tier_alter_image_link_date_expiration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="link_date_expiration",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 2, 24, 18, 10, 59, 350658)
            ),
        ),
    ]