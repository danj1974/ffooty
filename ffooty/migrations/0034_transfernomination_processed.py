# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0033_auto_20160202_0032'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfernomination',
            name='processed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
