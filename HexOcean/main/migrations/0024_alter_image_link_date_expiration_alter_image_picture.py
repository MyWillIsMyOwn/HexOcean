# Generated by Django 4.1.7 on 2023-02-24 18:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0023_alter_image_link_date_expiration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="link_date_expiration",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 2, 24, 18, 20, 37, 624505)
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="picture",
            field=models.ImageField(
                upload_to="images/%Y/%m/%d/%H-%M-%S-3b365dce-8613-45cf-9024-ea2b8503c178"
            ),
        ),
    ]
