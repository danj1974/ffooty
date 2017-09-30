# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0014_auto_20150805_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='funds',
            field=models.DecimalField(default=0, max_digits=4, decimal_places=1),
        ),
    ]
