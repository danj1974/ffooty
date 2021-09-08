# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0051_premteam_web_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[('1', 'GKP'), ('2', 'DEF'), ('3', 'MID'), ('4', 'STR')]),
        ),
        migrations.AlterField(
            model_name='teamtotalscorearchive',
            name='year',
            field=models.IntegerField(default=2021, max_length=4, choices=[(2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029)]),
        ),
    ]
