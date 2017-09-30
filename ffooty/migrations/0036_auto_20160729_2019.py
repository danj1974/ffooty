# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def team_changes_2016(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    PremTeam = apps.get_model("ffooty", "PremTeam")

    relegated_team_codes = ['AVL', 'NEW', 'NOR']

    for code in relegated_team_codes:
        team = PremTeam.objects.get(code=code)
        team.is_prem = False
        team.save()

    promoted_team_codes = ['BUR', 'HUL']

    for code in promoted_team_codes:
        team = PremTeam.objects.get(code=code)
        team.is_prem = True
        team.save()

    # new team
    PremTeam.objects.create(name='Middlesbrough', code='MID', is_prem=True)


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0035_team_cup_start_position'),
    ]

    operations = [
        migrations.RunPython(team_changes_2016)
    ]
