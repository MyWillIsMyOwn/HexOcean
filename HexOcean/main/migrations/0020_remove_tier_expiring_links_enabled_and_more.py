# Generated by Django 4.1.7 on 2023-02-21 17:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0019_tier_thumbnails_alter_image_link_date_expiration"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tier",
            name="expiring_links_enabled",
        ),
        migrations.RemoveField(
            model_name="tier",
            name="middle_thumbnail_size",
        ),
        migrations.RemoveField(
            model_name="tier",
            name="original_link_enabled",
        ),
        migrations.RemoveField(
            model_name="tier",
            name="small_thumbnail_size",
        ),
        migrations.AlterField(
            model_name="image",
            name="link_date_expiration",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 2, 21, 17, 39, 5, 357106)
            ),
        ),
        migrations.AlterField(
            model_name="tier",
            name="thumbnails",
            field=models.JSONField(
                default={
                    "expiring_links_enabled": False,
                    "original_link_enabled": True,
                    "thumbnails": [
                        {"name": "small", "size": 200},
                        {"name": "big", "size": 400},
                        {"name": "huge", "size": 800},
                    ],
                }
            ),
        ),
    ]
