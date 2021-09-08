# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0019_player_total_score_counted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='week',
            options={'ordering': ['number']},
        ),
        migrations.AlterField(
            model_name='playerscore',
            name='player',
            field=models.ForeignKey(related_name='scores', to='ffooty.Player', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='transfernomination',
            name='transfer_window',
            field=models.ForeignKey(blank=True, to='ffooty.TransferWindow', null=True, on_delete=models.CASCADE),
        ),
    ]
