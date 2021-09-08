# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0002_auto_20150716_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='prem_team',
            field=models.ForeignKey(related_name='players', to='ffooty.PremTeam', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='player',
            name='sale',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='team',
            field=models.ForeignKey(related_name='players', blank=True, to='ffooty.Team', null=True, on_delete=models.CASCADE),
        ),
    ]
