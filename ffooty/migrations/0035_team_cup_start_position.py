# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0034_transfernomination_processed'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='cup_start_position',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
