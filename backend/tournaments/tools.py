from . import models
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


  
