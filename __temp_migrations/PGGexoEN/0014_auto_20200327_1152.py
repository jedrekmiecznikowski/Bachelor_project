# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-03-27 10:52
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('PGGexoEN', '0013_auto_20200327_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='paid',
            field=otree.db.models.PositiveIntegerField(null=True),
        ),
    ]