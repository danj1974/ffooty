# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0031_auto_20160131_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerteamscore',
            name='player',
            field=models.ForeignKey(related_name=b'player_team_scores', to='ffooty.Player'),
        ),
        migrations.AlterField(
            model_name='playerteamscore',
            name='team',
            field=models.ForeignKey(related_name=b'player_team_scores', to='ffooty.Team'),
        ),
    ]
