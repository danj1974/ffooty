# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0042_player_appearances'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='auctionnomination',
            unique_together=None,
        ),
        migrations.AlterUniqueTogether(
            name='transfernomination',
            unique_together=None,
        ),
    ]
