# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2020-03-30 10:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PGGRegiEN', '0025_auto_20200327_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='business',
        ),
        migrations.RemoveField(
            model_name='player',
            name='economics',
        ),
    ]
