# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-03-27 15:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PGGexoEN', '0025_remove_player_earnings_last_round'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='comprehension1',
        ),
        migrations.RemoveField(
            model_name='player',
            name='comprehension2',
        ),
        migrations.RemoveField(
            model_name='player',
            name='comprehension3',
        ),
    ]