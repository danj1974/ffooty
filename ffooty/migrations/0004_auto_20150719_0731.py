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
            field=models.CharField(blank=True, max_length=1, null=True, choices=[('A', 'Available'), ('F', 'First Team'), ('R', 'Reserve'), ('S', 'Squad')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='status',
            field=models.CharField(default='A', max_length=1, blank=True, choices=[('A', 'Available'), ('F', 'First Team'), ('R', 'Reserve'), ('S', 'Squad')]),
        ),
    ]
