# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0032_auto_20160201_0025'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='playerscore',
            unique_together=set([('player', 'week', 'team')]),
        ),
    ]
