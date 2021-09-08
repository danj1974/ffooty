# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0005_auto_20150719_0740'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('type', models.CharField(default='N', max_length=1, choices=[('B', 'Boolean'), ('D', 'Date'), ('N', 'Number'), ('T', 'Text')])),
                ('description', models.TextField(null=True, blank=True)),
                ('boolean_value', models.NullBooleanField()),
                ('date_value', models.DateField(null=True, blank=True)),
                ('number_value', models.FloatField(null=True, blank=True)),
                ('text_value', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[('G', 'GKP'), ('D', 'DEF'), ('M', 'MID'), ('S', 'STR')]),
        ),
    ]
