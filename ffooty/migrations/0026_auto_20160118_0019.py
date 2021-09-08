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
            field=models.ForeignKey(blank=True, to='ffooty.Team', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transfernomination',
            name='status',
            field=models.CharField(default='N', max_length=1, choices=[('N', 'Pending'), ('H', 'Highest'), ('L', 'List'), ('O', 'Outbid'), ('P', 'Passed'), ('A', 'Accepted'), ('F', 'Bid Failed')]),
        ),
        migrations.AlterField(
            model_name='window',
            name='type',
            field=models.CharField(default='S', max_length=1, choices=[('A', 'Auction Nomination'), ('S', 'Squad Change'), ('T', 'Transfer Nomination'), ('C', 'Transfer Confirmation')]),
        ),
    ]
