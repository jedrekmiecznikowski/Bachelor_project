# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-03-27 12:24
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('PGGexoEN', '0016_auto_20200327_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='comprehension1',
            field=otree.db.models.PositiveIntegerField(null=True, verbose_name='If you invested 30 tokens in the public good, how much of your income do you still have left (before the payment of the bonus or refund of the contributions)?'),
        ),
    ]
