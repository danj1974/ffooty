# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0018_auto_20150810_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='total_score_counted',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
