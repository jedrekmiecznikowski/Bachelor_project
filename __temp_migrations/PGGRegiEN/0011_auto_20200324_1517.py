# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-03-24 14:17
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('PGGRegiEN', '0010_auto_20200324_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='student',
            field=otree.db.models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], verbose_name=''),
        ),
    ]