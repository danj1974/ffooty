# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0015_auto_20150805_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='total_score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='playerscore',
            unique_together=set([('player', 'week')]),
        ),
    ]
