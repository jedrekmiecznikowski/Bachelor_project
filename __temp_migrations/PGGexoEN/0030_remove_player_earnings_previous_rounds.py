# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-03-30 20:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PGGexoEN', '0029_player_earnings_previous_rounds'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='earnings_previous_rounds',
        ),
    ]
