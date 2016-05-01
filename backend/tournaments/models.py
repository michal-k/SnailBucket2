from django.db import models
from django.contrib.auth.models import User

import datetime


class Member(models.Model):
  def __str__(self):
    return str(self.user)

  def name(self):
    return self.user.username

  user = models.OneToOneField(User, primary_key=True,
    help_text='Basic account information, username, password, email, etc.')

  country = models.CharField(max_length=2, null=True, blank=True,
    help_text='Two letter country code of the member. Lowercase.')

  suspended_until = models.DateField(null=True, blank=True,
    help_text='Until what date the user is suspended from games.')

  reliability = models.IntegerField(default=2,
                                    help_text='Reliability rating.')

  preferred_hours = models.CharField(max_length=24, default='y' * 24, help_text=
    '24-character string of format "yyyyyrrrrwwwwwwwwyyyyyyy", UTC-based.')

  preferred_control = models.CharField(default='45 45', max_length=100,
    help_text='Comma separated list of "MM SS" time controls.')


class Tournament(models.Model):
  def __str__(self):
    return "%s (%s)" % (str(self.name), str(self.short_name))

  short_name = models.SlugField(max_length=32,
    help_text='E.g. monthly15, sb4, etc.')

  name = models.CharField(max_length=160,
    help_text='Snail Bucket Monthly 2015')

  type_code = models.CharField(max_length=32,
    help_text='Tournament type code, e.g. "RR", "Swiss", etc.')

  signup_start = models.DateTimeField(help_text='When registration is open.')

  signup_end = models.DateTimeField(
    help_text='When registration is no longer open.')

  # The bucketgen_* fields are used to generate buckets.
  bucketgen_min_bucket_size = models.IntegerField(
    help_text='Minimum number of players in a bucket.')

  bucketgen_max_bucket_size = models.IntegerField(
    help_text='Maximum number of players in a bucket.')

  # The roundsgen_* fields is only used to generate rounds.
  roundsgen_games_start = models.DateTimeField(
    help_text='Round 1 won\'t start before that time')

  roundsgen_rounds_count = models.IntegerField(
    help_text='Number of rounds in the tournament.')

  roundsgen_rounds_start_cron = models.CharField(max_length=32,
    default='0 0 * * Wed',
    help_text='Starting date of every round, in crontab format. '
              'E.g. "0 0 * * Wed" for weekly or "0 0 3 * *" for monthly.')

  def games_left(self):
    """Returns number of games which don't have played_date set."""
    return Game.objects.filter(bucket__tournament=self).filter(
      played_time__isnull=True).count()

  def last_played_game_date(self):
    game = Game.objects.filter(bucket__tournament=self).filter(
      played_time__isnull=False).order_by('-played_time')[:1]
    if not game:
      return None
    return game[0].played_time

  def is_active(self):
    """Returns if a tournament is active.

    The tournament is active if one of those is true:
       * Signup already started but not finished.
       * There are rounds which start in a future.
       * There are games which don't have played_date set.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    if self.signup_start > now:
      return False  # Signup not yet started, the tournament is in future.
    if self.round_set.count() == 0:
      return True  # Rounds are not yet created, so the tournament is active.
    # Sort rounds in reverse order by start date.
    last_round_start = self.round_set.order_by('-start')[0].start
    if last_round_start > now:
      return True  # There are rounds which start in a future.
    # Tournament is active if there are still non-played games.
    return self.games_left() > 0


class Round(models.Model):
  tournament = models.ForeignKey(Tournament)

  start = models.DateTimeField(help_text='When the round starts.')


class Bucket(models.Model):
  def __str__(self):
    return "%s -- %s" % (str(self.tournament.name), str(self.name))

  tournament = models.ForeignKey(Tournament)

  name = models.CharField(max_length=64, help_text='Name of the bucket.')

  tds = models.ManyToManyField(Member)


class TournamentPlayer(models.Model):
  """ Contains player assignment to tournament / buckets. """
  def __str__(self):
    return str(self.member)

  tournament = models.ForeignKey(Tournament, related_name='players')

  bucket = models.ForeignKey(Bucket, null=True, blank=True,
    related_name='players', help_text='Player of which bucket.')

  member = models.ForeignKey(Member)

  fixed_rating = models.IntegerField(null=True, blank=True,
    help_text='Fixed raiting. If NULL, it means that the bot haven\'t filled '
              'the rating yet')


class Game(models.Model):
  def __str__(self):
    return "%s, R%d, %s vs %s (%s)" % (
      self.bucket, self.round,
      self.white_player, self.black_player, self.result)

  bucket = models.ForeignKey(Bucket)

  round = models.IntegerField(help_text='Which round is the game from.')

  white_player = models.ForeignKey(TournamentPlayer, null=True, blank=True,
    related_name='white_game',
    help_text='Player who plays as white. Can be null in case of a bye.')

  black_player = models.ForeignKey(TournamentPlayer, null=True, blank=True,
    related_name='black_game',
    help_text='Player who plays as black. Can be null in case of a bye.')

  scheduled_time = models.DateTimeField(null=True, blank=True,
    help_text='Scheduled date of a game.')

  played_time = models.DateTimeField(null=True, blank=True,
    help_text='Time when then game was finished (or adjudicated).')

  # TODO(crem) Enumerate possible game results.
  result = models.CharField(max_length=16,
    help_text='Game status/result.', choices=(
      ('1-0','1-0'), ('i-o','i-o'), ('+:-','+:-'), ('0-1','0-1'), ('o-i','o-i'),
      ('-:+','-:+'), ('o-o','o-o'), ('-:-','-:-'), ('1/2-1/2', '1/2-1/2'),
      ('i/2-i/2', 'i/2-i/2')), null=True, blank=True)

  pgn = models.TextField(null=True, blank=True, help_text='Game in PGN format.')


class GameForumMessage(models.Model):
  def __str__(self):
    return 'Message from %s, %s, %s' % (self.member, self.time, self.game)

  game = models.ForeignKey(Game)

  time = models.DateTimeField(help_text='Time of a message')

  member = models.ForeignKey(Member, null=True, blank=True,
    help_text='Author of a forum message, or NULL for bot message.')

  text = models.TextField(help_text='Text of the message.')

  game_time = models.DateTimeField(null=True, blank=True,
    help_text='Time of a game, if set in a message.')

  reset_game_time = models.BooleanField(default=False,
    help_text='Resets the time of a game. Only if game_time = NULL.')
