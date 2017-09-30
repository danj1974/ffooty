# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0008_auto_20150727_0127'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('name', 'prem_team')]),
        ),
    ]
