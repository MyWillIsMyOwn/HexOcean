# Generated by Django 4.1.7 on 2023-02-26 21:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_alter_image_link_date_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='link_date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 26, 21, 38, 19, 177844)),
        ),
    ]
