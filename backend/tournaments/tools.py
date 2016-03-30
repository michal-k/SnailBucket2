from . import models
from croniter import croniter
import datetime

class NotFound(Exception):
  """Exception which is thrown when something is not found."""


class PermissionDenied(Exception):
  """Exception thrown when someone doesn't have permission to do something."""


def get_tournament(tournament):
  """Gets tournament model instance.

  Arguments:
    tournament -- short name of tournament.
  Return:
    models.Tournament object instance.
  Throws:
    NotFound -- if tournament is not found.
  """
  try:
    return models.Tournament.objects.get(short_name=tournament)
  except models.Tournament.DoesNotExist:
    raise NotFound("Tournament [%s] is not found." % tournament)


def get_game(game_id):
  """Gets game model instance.

  Arguments:
    game_id -- numeric id of a game.
  Throws:
    NotFound -- if game is not found.
  """
  try:
    return models.Game.objects.get(id=game_id)
  except models.Game.DoesNotExist:
    raise NotFound("Game [%d] is not found." % game_id)


def get_member(user):
  """Returns member object from user.

  Arguments:
    user -- user model object.
  Throws:
    NotFound -- if user doesn't have corresponding user.
  """
  if not user:
    raise PermissionDenied('No user specified.')
  # Users who are not logged in are not tournament members.
  if not user.is_authenticated():
    raise PermissionDenied('User not authenticated')
  try:
    return models.Member.objects.get(user=user)
  except models.Member.DoesNotExist:
    raise NotFound("User [%s] does not have corresponding member."
                   % user.username)


def get_tournament_buckets(tournament):
  """Return list of bucket of a given tournament, with list of participants per
  bucket.

  Arguments:
    tournament -- short_name of a tournament.
  Return:
    List of dictionaries [{'name': <tournament name>,
                           'members': [{
                              'name': <player name>,
                              'country': <player country code>,
                              'rating': <fixed rating>
                              }, ...]}, ...]
  Throws:
    NotFound -- if tournament is not found.
  """
  ratings = {}
  for player in get_tournament(tournament).players.all():
    ratings[player.member.name()] = player.fixed_rating
  buckets = get_tournament(tournament).bucket_set.all()
  return [
      { 'name': b.name,
        'members': [ 
      { 'name': m.member.name(),
        'country': m.member.country,
        'rating': ratings[m.member.name()] }
      for m in b.players.all() ] }
      for b in buckets ]


def get_tournament_participants(tournament):
  """Return the list of participants for a given tournament.

  Arguments:
    tournament -- short_name of a tournament.
  Return:
    List of dictionaries [{'name': <player_name>,
         'country': <country_code>,
         'rating': <player_rating>}, ...]
  Throws:
    NotFound -- if tournamnet is not found.
  """
  return [ 
      { 'name': player.member.name(),
        'rating': player.fixed_rating,
        'country': player.member.country }
    for player in get_tournament(tournament).players.all()]


def add_forum_message(game, member, text='',
                      month=0, day=0, hour=0, minute=0, reset=False):
  """Adds forum message.

  Arguments:
    game -- game object.
    member -- member object.
    text -- text to add.
    month, day, hour, minute -- if not zero, add that as game time.
    reset -- reset game time.
  Return:
    None
  Throws:
    PermissionDenied -- if user doesn't have permission to add message.
  """
  # User must be one of players or one of TDs for that bucket.
  if (member != game.white_player and
      member != game.black_player and
      member not in [t for t in game.bucket.tds.all()]):
    raise PermissionDenied("User %s doesn't have permission to access game %d."
                           % (member.user.username, game_id))
  message = models.GameForumMessage(
    game=game, member=member, text=text, time=datetime.datetime.now())
  if reset:
    message.reset_game_time = True
  else:
    year = datetime.date.today().year
    # If months is in the past, then year is the next year.
    if month < datetime.date.today().month:
      year += 1
    # If month and day are zero, don't set it.
    if month > 0 and day > 0:
      message.game_time = datetime.datetime(year, month, day, hour, minute)
  message.save()


def get_tournaments(only_active=False):
  """Returns the list of tournaments, except for future ones
  (ones which have signup date in future)

  Arguments:
    only_active -- only return active tournaments. Active tournaments are:
                   * With signup started but not finished
                   * Last game played < 30 days ago
                   * There are unplayed games
                   * There are rounds which start in a future
                   If there is no active tournaments, the tournament which
                   was finished last is returned.
  Return:
    List of tournaments [{'id': <short name of a tournament>,
                          'name': <readable name of a tournament>,
                          'rounds': <total number of rounds>,
                          'started_rounds': <number of started rounds>,
                          'signup': <are sign ups currently allowed>}]
  """
  now = datetime.datetime.now(datetime.timezone.utc)
  tournaments = models.Tournament.objects.all()
  res = []

  was_active_game = False

  for t in tournaments:
    if t.signup_start >= now:
      continue  # Signup not yet started.    
    rounds = t.round_set.order_by('-start')
    j = {'active': t.is_active(),
         'id': t.short_name,
         'name': t.name,
         'signup': now < t.signup_end,
         'rounds': len(rounds),
         'started_rounds': len([r for r in rounds if r.start <= now])}
    if not j['active']:
      j['last_game'] = t.last_played_game_date()
      if j['last_game'] and now - j['last_game'] < datetime.timedelta(days=30):
        # Recently finished tournaments are considered active.
        j['active'] = True
    was_active_game |= j['active']
    res.append(j)

  if only_active and res:
    if was_active_game:
      res = [t for t in res if t['active']]
    else:
      res = [max(res, key=lambda t: t['last_game'])]
  for t in res:
    del t['active']
    t.pop('end_date', None)
  return res


def get_pairings(tournament, round):
  """Returns pairings for a given round.

  Arguments:
   tournament -- tournament id
   round -- index of a round (1-based)

  Return:
   Dictionary: {
     'tournament_id': <id>
     'tournament_name': <long tournament name>
     'round': round index,
     'buckets': [{
       'bucket': <bucket name>,
       'games': [{
          'id': <game id>
          'white': <white player username, or None if round is bye>,
          'black': <black player username, or None if round is bye>,
          'white_country': <white player country code, or None>
          'black_country': <black player country code, or None>
          'result': <string which represents the game result>
          'scheduled_time': <timestamp of the game scheduled date>
          'played_time': <timestamp of the game finish date>
       }]
     }]
   }

  Throws:
    NotFound -- if tournament or round is not found.   
  """
  round = int(round)
  tournament = get_tournament(tournament)
  tournaments_round_count = tournament.round_set.count()
  if round < 1 or round > tournaments_round_count:
    raise NotFound("Tournament [%s] does not have round %d." % 
      (tournament, round))
  res = {
    'tournament_id': tournament.short_name,
    'tournament_name': tournament.name,
    'round': round,
    'buckets': []}
  for b in tournament.bucket_set.all():
    bucket = {'bucket': b.name, 'games': []}
    res['buckets'].append(bucket)
    games = bucket['games']
    for g in b.game_set.filter(round=round):
      games.append({
        'id': g.id,
        'white': g.white_player.member.name(),
        'white_country': (g.white_player.member.country
                         if g.white_player else None),
        'black': g.black_player.member.name(),
        'black_country': (g.black_player.member.country
                         if g.black_player else None),        
        'scheduled_time': (g.scheduled_time.timestamp()
                           if g.scheduled_time else None),
        'played_time': g.played_time.timestamp() if g.played_time else None,
        'result': g.result})
  return res


def generate_tournament_rounds(pk):
  """Generates round schedule for a tournament based on the settings.

  Old schedule will be removed if it exists.
  """
  tournament = models.Tournament.objects.get(id=pk)
  base = tournament.roundsgen_games_start
  cron_expr = tournament.roundsgen_rounds_start_cron
  round_count = tournament.roundsgen_rounds_count
  itr = croniter(cron_expr, base)
  rounds = [itr.get_next(datetime.datetime) for i in range(round_count)]
  # Delete existing rounds if they exist.
  models.Round.objects.filter(tournament=tournament).delete()
  # Add generated rounds.
  for r in rounds:
    round = models.Round.objects.create(tournament=tournament, start = r)
    round.save()
