# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0039_tableposition'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamTablePosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_week', models.IntegerField()),
                ('previous_week', models.IntegerField()),
                ('team', models.ForeignKey(to='ffooty.Team', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='tableposition',
            name='team',
        ),
        migrations.DeleteModel(
            name='TablePosition',
        ),
    ]
