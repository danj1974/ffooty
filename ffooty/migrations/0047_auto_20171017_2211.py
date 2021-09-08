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
                ('current_status', models.CharField(max_length=1, choices=[('A', 'Available'), ('F', 'First Team'), ('R', 'Reserve'), ('S', 'Squad')])),
                ('new_status', models.CharField(max_length=1, choices=[('A', 'Available'), ('F', 'First Team'), ('R', 'Reserve'), ('S', 'Squad')])),
                ('month', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('processed', models.BooleanField(default=False)),
                ('player', models.ForeignKey(to='ffooty.Player', on_delete=models.CASCADE)),
                ('window', models.ForeignKey(to='ffooty.Window', on_delete=models.CASCADE)),
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
