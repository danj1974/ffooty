# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0004_auto_20150719_0731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[('G', 'Goalkeeper'), ('D', 'Defender'), ('M', 'Midfielder'), ('S', 'Striker')]),
        ),
    ]
