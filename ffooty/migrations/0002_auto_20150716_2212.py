# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='money',
        ),
        migrations.AddField(
            model_name='team',
            name='funds',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='winnings',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
