# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ffooty', '0026_auto_20160118_0019'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMonthlyScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(null=True, blank=True)),
                ('month', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('team', models.ForeignKey(to='ffooty.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='teammonthlyscore',
            unique_together=set([('team', 'month')]),
        ),
    ]
