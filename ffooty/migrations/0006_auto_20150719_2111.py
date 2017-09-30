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
                ('type', models.CharField(default=b'N', max_length=1, choices=[(b'B', b'Boolean'), (b'D', b'Date'), (b'N', b'Number'), (b'T', b'Text')])),
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
            field=models.CharField(blank=True, max_length=1, null=True, choices=[(b'G', b'GKP'), (b'D', b'DEF'), (b'M', b'MID'), (b'S', b'STR')]),
        ),
    ]
