# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def load_teams(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    PremTeam = apps.get_model("ffooty", "PremTeam")

    # list of PremTeams to add
    team_list = [
        {'name': 'Arsenal', 'code': 'ARS', 'is_prem': True},
        {'name': 'Aston Villa', 'code': 'AVL', 'is_prem': True},
        {'name': 'Bournemouth', 'code': 'BOU', 'is_prem': True},
        {'name': 'Chelsea', 'code': 'CHE', 'is_prem': True},
        {'name': 'Crystal Palace', 'code': 'CRY', 'is_prem': True},
        {'name': 'Everton', 'code': 'EVE', 'is_prem': True},
        {'name': 'Hull', 'code': 'HUL', 'is_prem': False},
        {'name': 'Leicester City', 'code': 'LEI', 'is_prem': True},
        {'name': 'Liverpool', 'code': 'LIV', 'is_prem': True},
        {'name': 'Manchester City', 'code': 'MCY', 'is_prem': True},
        {'name': 'Manchester United', 'code': 'MUN', 'is_prem': True},
        {'name': 'Newcastle United', 'code': 'NEW', 'is_prem': True},
        {'name': 'Norwich City', 'code': 'NOR', 'is_prem': True},
        {'name': 'Queens Park Rangers', 'code': 'QPR', 'is_prem': False},
        {'name': 'Southampton', 'code': 'SOT', 'is_prem': True},
        {'name': 'Stoke City', 'code': 'STO', 'is_prem': True},
        {'name': 'Sunderland', 'code': 'SUN', 'is_prem': True},
        {'name': 'Swansea City', 'code': 'SWA', 'is_prem': True},
        {'name': 'Tottenham Hotspur', 'code': 'TOT', 'is_prem': True},
        {'name': 'Watford', 'code': 'WAT', 'is_prem': True},
        {'name': 'West Bromwich Albion', 'code': 'WBA', 'is_prem': True},
        {'name': 'West Ham United', 'code': 'WHM', 'is_prem': True},
        {'name': 'Burnley', 'code': 'BUR', 'is_prem': False},
    ]

    for team in team_list:
        print(PremTeam.objects.update_or_create(name=team['name'], code=team['code'], is_prem=team['is_prem']))
        # print(pt, created)


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0006_auto_20150719_2111'),
    ]

    operations = [
        migrations.RunPython(load_teams),
    ]
