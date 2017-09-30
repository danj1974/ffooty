# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0013_auto_20150805_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='sale',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='value',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='winnings',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='transfernomination',
            name='bid',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1),
        ),
    ]
