# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0036_auto_20160729_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='last_years_total',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
