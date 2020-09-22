# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0049_auto_20200915_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='web_code',
            field=models.IntegerField(unique=True, null=True),
        ),
    ]
