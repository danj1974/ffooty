# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0047_auto_20171017_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionnomination',
            name='passed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='teamtotalscorearchive',
            name='year',
            field=models.IntegerField(default=2019, max_length=4, choices=[(2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029)]),
        ),
    ]
