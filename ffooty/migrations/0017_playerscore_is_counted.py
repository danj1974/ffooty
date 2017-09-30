# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0016_auto_20150810_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerscore',
            name='is_counted',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
