from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
  user = models.OneToOneField(User, primary_key=True,
    help_text='Basic account information, username, password, email, etc.')

  country = models.CharField(max_length=2, null=True, blank=True,
    help_text='Two letter country code of the member. Lowercase.')

  suspended_until = models.DateField(null=True, blank=True,
    help_text='Until what date the user is suspended from games.')

  reliability = models.IntegerField(help_text='Reliability rating.')

  preferred_hours = models.CharField(max_length=24, default='y' * 24, help_text=
    '24-character string of format "yyyyyrrrrwwwwwwwwyyyyyyy", UTC-based.')

  preferred_control = models.CharField(default='45 45', max_length=100,
    help_text='Comma separated list of ‘MM SS’ time controls.')

  # TODO(crem): Do we need `status` here?


class Tournament(models.Model):
  short_name = models.SlugField(max_length=32,
    help_text='E.g. monthly15, sb4, etc.')

  name = models.CharField(max_length=160,
    help_text='Snail Bucket Monthly 2015')

  type_code = models.CharField(max_length=32,
    help_text='Tournament type code, e.g. "RR", "Swiss", etc.')

  signup_start = models.DateTimeField(help_text='When registration is open.')

  signup_end = models.DateTimeField(
    help_text='When registration is no longer open.')

  games_start = models.DateTimeField(
    help_text='Round 1 won\'t start before that time')

  rounds_count = models.IntegerField(
    help_text='Number of rounds in the tournament.')

  rounds_start_cron = models.CharField(max_length=32,
    help_text='Starting date of every round, in crontab format.')

  min_bucket_size = models.IntegerField(
    help_text='Minimum number of players in a bucket.')

  max_bucket_size = models.IntegerField(
    help_text='Maximum number of players in a bucket.')


class Round(models.Model):
  tournament = models.ForeignKey(Tournament)

  start = models.DateTimeField(help_text='When the round starts.')


class Bucket(models.Model):
  tournament = models.ForeignKey(Tournament)

  name = models.CharField(max_length=64, help_text='Name of the bucket.')

  tds = models.ManyToManyField(Member)


class BucketPlayer(models.Model):
  bucket = models.ForeignKey(Bucket, related_name='players',
    help_text='Player of which bucket.')

  member = models.ForeignKey(Member, help_text='Which user.')

  # TODO(crem): Do we need `status` here?


class TournamentPlayer(models.Model):
  """ Contains players before the split into buckets occurred. """
  tournament = models.ForeignKey(Tournament, related_name='players')

  member = models.ForeignKey(Tournament)

  fixed_rating = models.IntegerField(null=True, blank=True,
    help_text='Fixed raiting. If NULL, it means that the bot haven\'t filled '
              'the rating yet')


class Game(models.Model):
  bucket = models.ForeignKey(Bucket)

  round = models.IntegerField(help_text='Which round is the game from.')

  white_player = models.ForeignKey(Member, null=True, blank=True,
    related_name='white_game',
    help_text='Player who plays as white. Can be null in case of a bye.')

  black_player = models.ForeignKey(Member, null=True, blank=True,
    related_name='black_game',
    help_text='Player who plays as black. Can be null in case of a bye.')

  scheduled_time = models.DateTimeField(null=True, blank=True,
    help_text='Scheduled date of a game.')

  played_time = models.DateTimeField(null=True, blank=True,
    help_text='Time when then game was finished.')

  # TODO(crem) Enumerate possible game results.
  result = models.CharField(max_length=16,
    help_text='Game status/result.')

  pgn = models.TextField(null=True, blank=True, help_text='Game in PGN format.')


class GameForumMessage(models.Model):
  game = models.ForeignKey(Game)

  time = models.DateTimeField(help_text='Time of a message')

  member = models.ForeignKey(Member, null=True, blank=True,
    help_text='Author of a forum message, or NULL for bot message.')

  text = models.TextField(help_text='Text of the message.')

  game_time = models.DateTimeField(null=True, blank=True,
    help_text='Time of a game, if set in a message.')

  reset_game_time = models.BooleanField(default=False,
    help_text='Resets the time of a game. Only if game_time = NULL.')








