# Generated by Django 2.1.2 on 2018-10-25 12:41

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20181025_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.UUIDField(default=account.models.get_token, editable=False, unique=True),
        ),
    ]
