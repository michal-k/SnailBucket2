from . import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
import json
import datetime

def get_participants(request, tournament):
  buckets = get_object_or_404(models.Tournament, short_name=tournament
    ).bucket_set.all()
  res = [ { 'name': b.name,
            'members': [ m.member.name() for m in b.players.all() ] }
          for b in buckets ]
  return HttpResponse(json.dumps(res))


def add_forum_message(request, game_id):
  # Users who are not logged in cannot add forum messages.
  if not request.user.is_authenticated():
    raise PermissionDenied
  game = get_object_or_404(models.Game, id=game_id)

  # User must be one of players or one of TDs for that bucket.
  if (request.user != game.white_player.user and
      request.user != game.black_player.user and
      request.user not in [t.user for t in game.bucket.tds.all()]):
    raise PermissionDenied

  # Convert user object to member object
  try:
    member = models.Member.objects.get(user=request.user)
  except modeks.Member.DoesNotExist:
    return HttpResponse(status=500)

  query = request.GET
  # Forum message text is a required parameter.
  try:
    text = query['text']
  except:
    return HttpResponse(status=422)

  message = models.GameForumMessage(
    game=game, member=member, text=text, time=datetime.datetime.now())

  if query.get('reset', '') == '1':
    # This query has 'reset' flag.
    message.reset_game_time = True
  else:
    try:
      month = int(query.get('month', '0'))
      day = int(query.get('day', '0'))
      hour = int(query.get('hour', '0'))
      minute = int(query.get('minute', '0'))
      year = datetime.date.today().year
      if month < datetime.date.today().month:
        year += 1
      if month > 0 and day > 0:
        message.game_time = datetime.datetime(year, month, day, hour, minute)
    except:
      return HttpResponse(status=422)

  message.save()

  # TODO(crem): Or what would be more appropriate response text?
  return HttpResponse('OK!')