# Generated by Django 2.1.2 on 2018-11-05 17:18

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20181105_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributevalue',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True),
        ),
    ]