# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0007_load_prem_teams_20150727_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='code',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='auctionnomination',
            unique_together=set([('team', 'player')]),
        ),
        migrations.AlterUniqueTogether(
            name='transfernomination',
            unique_together=set([('team', 'player')]),
        ),
    ]
