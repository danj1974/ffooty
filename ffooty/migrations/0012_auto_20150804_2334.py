# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0011_player_is_new'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['manager__username']},
        ),
    ]
