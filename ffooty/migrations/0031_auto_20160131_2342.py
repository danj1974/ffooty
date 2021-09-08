# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0030_remove_player_total_score_counted'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerTeamScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(null=True, blank=True)),
                ('player', models.ForeignKey(related_name='team_scores', to='ffooty.Player', on_delete=models.CASCADE)),
                ('team', models.ForeignKey(related_name='player_scores', to='ffooty.Team', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='teammonthlyscore',
            name='team',
            field=models.ForeignKey(related_name='monthly_scores', to='ffooty.Team', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='teamweeklyscore',
            name='team',
            field=models.ForeignKey(related_name='weekly_scores', to='ffooty.Team', on_delete=models.CASCADE),
        ),
    ]
