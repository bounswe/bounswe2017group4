# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-11 12:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatBot', '0002_auto_20171111_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telegram_id',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
