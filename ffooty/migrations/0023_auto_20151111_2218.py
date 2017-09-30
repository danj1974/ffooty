# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0022_team_loss'),
    ]

    operations = [
        migrations.AlterField(
            model_name='squadchange',
            name='open_from',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='squadchangewindow',
            name='open_from',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='transferwindow',
            name='open_from',
            field=models.DateTimeField(),
        ),
    ]
