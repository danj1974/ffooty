# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0040_auto_20160807_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='window',
            name='type',
            field=models.CharField(default='S', max_length=1, choices=[('N', 'Auction Nomination'), ('A', 'Auction'), ('S', 'Squad Change'), ('T', 'Transfer Nomination'), ('C', 'Transfer Confirmation')]),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('name', 'code')]),
        ),
    ]
