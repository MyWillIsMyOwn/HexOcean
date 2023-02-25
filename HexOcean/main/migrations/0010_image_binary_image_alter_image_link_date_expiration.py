# Generated by Django 4.1.7 on 2023-02-21 09:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_image_link_date_expiration"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="binary_image",
            field=models.BinaryField(null=True),
        ),
        migrations.AlterField(
            model_name="image",
            name="link_date_expiration",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 2, 21, 10, 24, 43, 26124)
            ),
        ),
    ]
