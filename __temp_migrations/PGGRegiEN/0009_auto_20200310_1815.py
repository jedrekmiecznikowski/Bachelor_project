# Generated by Django 2.2.4 on 2020-03-10 17:15

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('PGGRegiEN', '0008_remove_player_rulestr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='rule',
        ),
        migrations.AddField(
            model_name='player',
            name='understand',
            field=otree.db.models.BooleanField(choices=[[True, 'Yes'], [False, 'No']], null=True),
        ),
    ]
