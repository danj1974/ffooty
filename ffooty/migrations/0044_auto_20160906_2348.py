# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0043_auto_20160906_2347'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='auctionnomination',
            unique_together=set([('team', 'player')]),
        ),
    ]
