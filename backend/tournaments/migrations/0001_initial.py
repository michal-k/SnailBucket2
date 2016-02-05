# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=64, help_text='Name of the bucket.')),
            ],
        ),
        migrations.CreateModel(
            name='BucketPlayer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('bucket', models.ForeignKey(to='tournaments.Bucket', related_name='players', help_text='Player of which bucket.')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('round', models.IntegerField(help_text='Which round is the game from.')),
                ('scheduled_time', models.DateTimeField(blank=True, help_text='Scheduled date of a game.', null=True)),
                ('played_time', models.DateTimeField(blank=True, help_text='Time when then game was finished.', null=True)),
                ('result', models.CharField(max_length=16, help_text='Game status/result.')),
                ('pgn', models.TextField(blank=True, help_text='Game in PGN format.', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameForumMessage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('time', models.DateTimeField(help_text='Time of a message')),
                ('text', models.TextField(help_text='Text of the message.')),
                ('game_time', models.DateTimeField(blank=True, help_text='Time of a game, if set in a message.', null=True)),
                ('reset_game_time', models.BooleanField(default=False, help_text='Resets the time of a game. Only if game_time = NULL.')),
                ('game', models.ForeignKey(to='tournaments.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, help_text='Basic account information, username, password, email, etc.', to=settings.AUTH_USER_MODEL)),
                ('country', models.CharField(blank=True, max_length=2, help_text='Two letter country code of the member. Lowercase.', null=True)),
                ('suspended_until', models.DateField(blank=True, help_text='Until what date the user is suspended from games.', null=True)),
                ('reliability', models.IntegerField(help_text='Reliability rating.')),
                ('preferred_hours', models.CharField(default='yyyyyyyyyyyyyyyyyyyyyyyy', max_length=24, help_text='24-character string of format "yyyyyrrrrwwwwwwwwyyyyyyy", UTC-based.')),
                ('preferred_control', models.CharField(default='45 45', max_length=100, help_text='Comma separated list of ‘MM SS’ time controls.')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('start', models.DateTimeField(help_text='When the round starts.')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('short_name', models.SlugField(max_length=32, help_text='E.g. monthly15, sb4, etc.')),
                ('name', models.CharField(max_length=160, help_text='Snail Bucket Monthly 2015')),
                ('type_code', models.CharField(max_length=32, help_text='Tournament type code, e.g. "RR", "Swiss", etc.')),
                ('signup_start', models.DateTimeField(help_text='When registration is open.')),
                ('signup_end', models.DateTimeField(help_text='When registration is no longer open.')),
                ('games_start', models.DateTimeField(help_text="Round 1 won't start before that time")),
                ('rounds_count', models.IntegerField(help_text='Number of rounds in the tournament.')),
                ('rounds_start_cron', models.CharField(max_length=32, help_text='Starting date of every round, in crontab format.')),
                ('min_bucket_size', models.IntegerField(help_text='Minimum number of players in a bucket.')),
                ('max_bucket_size', models.IntegerField(help_text='Maximum number of players in a bucket.')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentPlayer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('fixed_rating', models.IntegerField(blank=True, help_text="Fixed raiting. If NULL, it means that the bot haven't filled the rating yet", null=True)),
                ('member', models.ForeignKey(to='tournaments.Member')),
                ('tournament', models.ForeignKey(to='tournaments.Tournament', related_name='players')),
            ],
        ),
        migrations.AddField(
            model_name='round',
            name='tournament',
            field=models.ForeignKey(to='tournaments.Tournament'),
        ),
        migrations.AddField(
            model_name='gameforummessage',
            name='member',
            field=models.ForeignKey(to='tournaments.Member', null=True, help_text='Author of a forum message, or NULL for bot message.', blank=True),
        ),
        migrations.AddField(
            model_name='game',
            name='black_player',
            field=models.ForeignKey(to='tournaments.Member', null=True, related_name='black_game', help_text='Player who plays as black. Can be null in case of a bye.', blank=True),
        ),
        migrations.AddField(
            model_name='game',
            name='bucket',
            field=models.ForeignKey(to='tournaments.Bucket'),
        ),
        migrations.AddField(
            model_name='game',
            name='white_player',
            field=models.ForeignKey(to='tournaments.Member', null=True, related_name='white_game', help_text='Player who plays as white. Can be null in case of a bye.', blank=True),
        ),
        migrations.AddField(
            model_name='bucketplayer',
            name='member',
            field=models.ForeignKey(to='tournaments.Member', help_text='Which user.'),
        ),
        migrations.AddField(
            model_name='bucket',
            name='tds',
            field=models.ManyToManyField(to='tournaments.Member'),
        ),
        migrations.AddField(
            model_name='bucket',
            name='tournament',
            field=models.ForeignKey(to='tournaments.Tournament'),
        ),
    ]
