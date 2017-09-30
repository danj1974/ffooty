# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0010_auto_20150727_0137'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_new',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
