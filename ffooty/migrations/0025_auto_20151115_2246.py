# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0024_auto_20151111_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transfernomination',
            name='outcome',
        ),
        migrations.AddField(
            model_name='transfernomination',
            name='status',
            field=models.CharField(default='N', max_length=1, choices=[('N', 'Pending'), ('H', 'Highest'), ('L', 'List'), ('O', 'Outbid'), ('P', 'Passed'), ('S', 'Accepted'), ('F', 'Bid Failed')]),
            preserve_default=True,
        ),
    ]
