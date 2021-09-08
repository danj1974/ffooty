# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0045_auto_20160906_2351'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamTotalScoreArchive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(null=True, blank=True)),
                ('year', models.IntegerField(default=2017, max_length=4, choices=[(2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029)])),
                ('team', models.ForeignKey(to='ffooty.Team', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='transfernomination',
            name='status',
            field=models.CharField(default='N', max_length=1, choices=[('N', 'Pending'), ('H', 'Highest'), ('J', 'Joint Highest'), ('L', 'List'), ('O', 'Outbid'), ('P', 'Passed'), ('A', 'Accepted'), ('F', 'Bid Failed')]),
        ),
    ]
