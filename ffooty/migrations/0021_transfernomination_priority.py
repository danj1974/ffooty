# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0020_auto_20150907_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfernomination',
            name='priority',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
