# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0025_auto_20151115_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerscore',
            name='team',
            field=models.ForeignKey(blank=True, to='ffooty.Team', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transfernomination',
            name='status',
            field=models.CharField(default=b'N', max_length=1, choices=[(b'N', b'Pending'), (b'H', b'Highest'), (b'L', b'List'), (b'O', b'Outbid'), (b'P', b'Passed'), (b'A', b'Accepted'), (b'F', b'Bid Failed')]),
        ),
        migrations.AlterField(
            model_name='window',
            name='type',
            field=models.CharField(default=b'S', max_length=1, choices=[(b'A', b'Auction Nomination'), (b'S', b'Squad Change'), (b'T', b'Transfer Nomination'), (b'C', b'Transfer Confirmation')]),
        ),
    ]
