# Generated by Django 2.2.4 on 2020-03-09 21:47

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('PGGRegiEN', '0004_auto_20200305_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='rule',
            field=otree.db.models.PositiveIntegerField(choices=[[1, 'Yes'], [2, 'No']], null=True),
        ),
    ]
