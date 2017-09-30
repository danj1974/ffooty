# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0017_playerscore_is_counted'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamweeklyscore',
            name='week',
            field=models.ForeignKey(default=None, to='ffooty.Week'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='teamweeklyscore',
            unique_together=set([('team', 'week')]),
        ),
    ]
