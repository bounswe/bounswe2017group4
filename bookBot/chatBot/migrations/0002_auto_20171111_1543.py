# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-11 12:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatBot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('node_id', models.IntegerField()),
                ('user_response', models.CharField(max_length=200)),
                ('next_node_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('chatbot_response', models.CharField(max_length=500)),
                ('edge_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatBot.Edge')),
            ],
        ),
        migrations.DeleteModel(
            name='Nodes',
        ),
        migrations.AddField(
            model_name='user',
            name='telegram_id',
            field=models.IntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]
