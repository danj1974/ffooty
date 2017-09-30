# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0038_team_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='TablePosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_week', models.IntegerField()),
                ('previous_week', models.IntegerField()),
                ('team', models.ForeignKey(to='ffooty.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
