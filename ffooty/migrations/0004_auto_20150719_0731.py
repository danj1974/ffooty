# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0003_auto_20150716_2305'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ['code']},
        ),
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'A', b'Available'), (b'F', b'First Team'), (b'R', b'Reserve'), (b'S', b'Squad')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='status',
            field=models.CharField(default=b'A', max_length=1, blank=True, choices=[(b'A', b'Available'), (b'F', b'First Team'), (b'R', b'Reserve'), (b'S', b'Squad')]),
        ),
    ]
