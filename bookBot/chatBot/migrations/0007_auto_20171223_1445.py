# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-23 11:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatBot', '0006_auto_20171206_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
    ]
