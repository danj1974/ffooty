# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionNomination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Banter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['-added'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('banter', models.ForeignKey(related_name='comments', to='ffooty.Banter', null=True, on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('status', models.CharField(default='A', max_length=1, choices=[('A', 'Available'), ('F', 'First Team'), ('R', 'Reserve'), ('S', 'Squad')])),
                ('code', models.IntegerField(unique=True)),
                ('web_code', models.IntegerField(unique=True)),
                ('value', models.FloatField(null=True, blank=True)),
                ('sale', models.FloatField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(null=True, blank=True)),
                ('is_reserve', models.BooleanField(default=False)),
                ('is_squad', models.BooleanField(default=False)),
                ('player', models.ForeignKey(to='ffooty.Player', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PremTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('is_prem', models.BooleanField(default=True)),
                ('code', models.CharField(unique=True, max_length=3)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SquadChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('open_from', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
                ('new_status', models.CharField(max_length=1, choices=[('A', 'Available'), ('F', 'First Team'), ('R', 'Reserve'), ('S', 'Squad')])),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SquadChangeWindow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('open_from', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('money', models.IntegerField(default=0)),
                ('line_up_is_valid', models.BooleanField(default=False)),
                ('manager', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamTotalScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(null=True, blank=True)),
                ('team', models.ForeignKey(to='ffooty.Team', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamWeeklyScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(null=True, blank=True)),
                ('team', models.ForeignKey(to='ffooty.Team', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransferNomination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('outcome', models.CharField(default='N', max_length=1, choices=[('N', 'Pending'), ('S', 'Success'), ('L', 'List'), ('O', 'Outbid'), ('P', 'Pass')])),
                ('bid', models.FloatField(null=True)),
                ('player', models.ForeignKey(to='ffooty.Player', on_delete=models.CASCADE)),
                ('team', models.ForeignKey(to='ffooty.Team', on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransferWindow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('open_from', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.IntegerField(unique=True)),
                ('date', models.DateField()),
                ('is_cup', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='transfernomination',
            name='transfer_window',
            field=models.ForeignKey(to='ffooty.TransferWindow', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='squadchange',
            name='new_team',
            field=models.ForeignKey(blank=True, to='ffooty.Team', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='squadchange',
            name='player',
            field=models.ForeignKey(to='ffooty.Player', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='squadchange',
            name='window',
            field=models.ForeignKey(to='ffooty.SquadChangeWindow', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playerscore',
            name='week',
            field=models.ForeignKey(to='ffooty.Week', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='prem_team',
            field=models.ForeignKey(related_name='players', blank=True, to='ffooty.PremTeam', null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(related_name='players', to='ffooty.Team', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auctionnomination',
            name='player',
            field=models.ForeignKey(to='ffooty.Player', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='auctionnomination',
            name='team',
            field=models.ForeignKey(to='ffooty.Team', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
