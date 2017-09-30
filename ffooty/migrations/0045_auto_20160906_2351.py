# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0044_auto_20160906_2348'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='transfernomination',
            unique_together=set([('team', 'player', 'bid')]),
        ),
    ]
