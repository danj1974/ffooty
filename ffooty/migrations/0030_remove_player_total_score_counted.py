# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0029_auto_20160128_2103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='total_score_counted',
        ),
    ]
