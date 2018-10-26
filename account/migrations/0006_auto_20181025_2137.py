# Generated by Django 2.1.2 on 2018-10-25 18:37

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20181025_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.UUIDField(default=account.models.get_token, editable=False, unique=True),
        ),
    ]
