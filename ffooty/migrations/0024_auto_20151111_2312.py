# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0023_auto_20151111_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Window',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('open_from', models.DateTimeField()),
                ('deadline', models.DateTimeField()),
                ('type', models.CharField(default=b'S', max_length=1, choices=[(b'A', b'Auction Nomination'), (b'S', b'Squad Change'), (b'T', b'Transfer Nomination')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='squadchange',
            name='new_team',
        ),
        migrations.RemoveField(
            model_name='squadchange',
            name='player',
        ),
        migrations.RemoveField(
            model_name='squadchange',
            name='window',
        ),
        migrations.DeleteModel(
            name='SquadChange',
        ),
        migrations.DeleteModel(
            name='SquadChangeWindow',
        ),
        migrations.AlterField(
            model_name='transfernomination',
            name='transfer_window',
            field=models.ForeignKey(blank=True, to='ffooty.Window', null=True),
        ),
        migrations.DeleteModel(
            name='TransferWindow',
        ),
    ]
