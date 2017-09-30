# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0012_auto_20150804_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constant',
            name='number_value',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='funds',
            field=models.DecimalField(default=0, max_digits=5, decimal_places=2),
        ),
    ]
