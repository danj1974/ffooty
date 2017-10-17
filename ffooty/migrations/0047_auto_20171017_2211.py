# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0046_auto_20170720_2323'),
    ]

    operations = [
        migrations.CreateModel(
            name='SquadChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_status', models.CharField(max_length=1, choices=[(b'A', b'Available'), (b'F', b'First Team'), (b'R', b'Reserve'), (b'S', b'Squad')])),
                ('new_status', models.CharField(max_length=1, choices=[(b'A', b'Available'), (b'F', b'First Team'), (b'R', b'Reserve'), (b'S', b'Squad')])),
                ('month', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('processed', models.BooleanField(default=False)),
                ('player', models.ForeignKey(to='ffooty.Player')),
                ('window', models.ForeignKey(to='ffooty.Window')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='squadchange',
            unique_together=set([('player', 'window')]),
        ),
    ]
