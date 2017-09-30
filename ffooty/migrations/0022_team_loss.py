# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0021_transfernomination_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='loss',
            field=models.DecimalField(default=0, help_text=b'Cumulative loss made selling players back to pool', max_digits=4, decimal_places=1),
            preserve_default=True,
        ),
    ]
