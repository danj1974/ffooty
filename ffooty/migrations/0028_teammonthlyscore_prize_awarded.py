# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0027_auto_20160118_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammonthlyscore',
            name='prize_awarded',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
