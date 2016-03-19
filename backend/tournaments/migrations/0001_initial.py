# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-19 12:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the bucket.', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round', models.IntegerField(help_text='Which round is the game from.')),
                ('scheduled_time', models.DateTimeField(blank=True, help_text='Scheduled date of a game.', null=True)),
                ('played_time', models.DateTimeField(blank=True, help_text='Time when then game was finished (or adjudicated).', null=True)),
                ('result', models.CharField(help_text='Game status/result.', max_length=16)),
                ('pgn', models.TextField(blank=True, help_text='Game in PGN format.', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameForumMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(help_text='Time of a message')),
                ('text', models.TextField(help_text='Text of the message.')),
                ('game_time', models.DateTimeField(blank=True, help_text='Time of a game, if set in a message.', null=True)),
                ('reset_game_time', models.BooleanField(default=False, help_text='Resets the time of a game. Only if game_time = NULL.')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user', models.OneToOneField(help_text='Basic account information, username, password, email, etc.', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('country', models.CharField(blank=True, help_text='Two letter country code of the member. Lowercase.', max_length=2, null=True)),
                ('suspended_until', models.DateField(blank=True, help_text='Until what date the user is suspended from games.', null=True)),
                ('reliability', models.IntegerField(help_text='Reliability rating.')),
                ('preferred_hours', models.CharField(default='yyyyyyyyyyyyyyyyyyyyyyyy', help_text='24-character string of format "yyyyyrrrrwwwwwwwwyyyyyyy", UTC-based.', max_length=24)),
                ('preferred_control', models.CharField(default='45 45', help_text='Comma separated list of "MM SS" time controls.', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(help_text='When the round starts.')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.SlugField(help_text='E.g. monthly15, sb4, etc.', max_length=32)),
                ('name', models.CharField(help_text='Snail Bucket Monthly 2015', max_length=160)),
                ('type_code', models.CharField(help_text='Tournament type code, e.g. "RR", "Swiss", etc.', max_length=32)),
                ('signup_start', models.DateTimeField(help_text='When registration is open.')),
                ('signup_end', models.DateTimeField(help_text='When registration is no longer open.')),
                ('bucketgen_min_bucket_size', models.IntegerField(help_text='Minimum number of players in a bucket.')),
                ('bucketgen_max_bucket_size', models.IntegerField(help_text='Maximum number of players in a bucket.')),
                ('roundsgen_games_start', models.DateTimeField(help_text="Round 1 won't start before that time")),
                ('roundsgen_rounds_count', models.IntegerField(help_text='Number of rounds in the tournament.')),
                ('roundsgen_rounds_start_cron', models.CharField(help_text='Starting date of every round, in crontab format.', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentPlayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fixed_rating', models.IntegerField(blank=True, help_text="Fixed raiting. If NULL, it means that the bot haven't filled the rating yet", null=True)),
                ('bucket', models.ForeignKey(blank=True, help_text='Player of which bucket.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='players', to='tournaments.Bucket')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.Member')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='tournaments.Tournament')),
            ],
        ),
        migrations.AddField(
            model_name='round',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.Tournament'),
        ),
        migrations.AddField(
            model_name='gameforummessage',
            name='member',
            field=models.ForeignKey(blank=True, help_text='Author of a forum message, or NULL for bot message.', null=True, on_delete=django.db.models.deletion.CASCADE, to='tournaments.Member'),
        ),
        migrations.AddField(
            model_name='game',
            name='black_player',
            field=models.ForeignKey(blank=True, help_text='Player who plays as black. Can be null in case of a bye.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='black_game', to='tournaments.TournamentPlayer'),
        ),
        migrations.AddField(
            model_name='game',
            name='bucket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.Bucket'),
        ),
        migrations.AddField(
            model_name='game',
            name='white_player',
            field=models.ForeignKey(blank=True, help_text='Player who plays as white. Can be null in case of a bye.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='white_game', to='tournaments.TournamentPlayer'),
        ),
        migrations.AddField(
            model_name='bucket',
            name='tds',
            field=models.ManyToManyField(to='tournaments.Member'),
        ),
        migrations.AddField(
            model_name='bucket',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournaments.Tournament'),
        ),
    ]
