# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-03-27 10:34
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('PGGRegiEN', '0020_auto_20200327_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='gender',
            field=otree.db.models.PositiveIntegerField(choices=[[0, 'Female'], [1, 'Male'], [2, 'Other']], null=True, verbose_name='Which semester are you on or how many semesters did you complete at a higher education facility?'),
        ),
        migrations.AlterField(
            model_name='player',
            name='semester',
            field=otree.db.models.IntegerField(null=True, verbose_name='Which semester are you on or how many semesters did you complete at a higher education facility?'),
        ),
    ]
