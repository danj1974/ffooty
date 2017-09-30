# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0041_auto_20160811_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='appearances',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
