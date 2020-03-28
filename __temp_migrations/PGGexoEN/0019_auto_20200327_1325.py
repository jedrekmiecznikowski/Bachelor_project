# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-03-27 12:25
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('PGGexoEN', '0018_auto_20200327_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='comprehension3',
            field=otree.db.models.PositiveIntegerField(null=True, verbose_name='The number of people, threshold, your income and contributions of the other people are the same as in question 2. Your contribution is different - it is 40 tokens. What is your payoff for this round?'),
        ),
    ]