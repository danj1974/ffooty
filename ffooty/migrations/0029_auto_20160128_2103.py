# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0028_teammonthlyscore_prize_awarded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerscore',
            name='is_counted',
            field=models.BooleanField(default=False),
        ),
    ]
