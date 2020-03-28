# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-03-27 10:33
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('PGGRegiEN', '0018_player_contribution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='contribution',
        ),
        migrations.AddField(
            model_name='player',
            name='gender',
            field=otree.db.models.PositiveIntegerField(choices=[[0, 'Female'], [1, 'Male'], [2, 'Other']], null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='semester',
            field=otree.db.models.IntegerField(null=True),
        ),
    ]