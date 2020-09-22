# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0050_auto_20200915_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='premteam',
            name='web_code',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
