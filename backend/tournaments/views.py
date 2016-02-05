from . import tools
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
import json

def get_participants(request, tournament):
  try:
    res = tools.get_tournament_buckets(tournament)
  except tools.NotFound:
    raise Http404
  return HttpResponse(json.dumps(res))


def add_forum_message(request, game_id):
  try:
    game = tools.get_game(game_id)
    member = tools.get_member(request.user)

    query = request.GET
    # Forum message text is a required parameter.
    try:
      text = query['text']
      reset = (query.get('reset', '') == '1')
      month = int(query.get('month', '0'))
      day = int(query.get('day', '0'))
      hour = int(query.get('hour', '0'))
      minute = int(query.get('minute', '0'))
    except:
      return HttpResponse(status=422)

    tools.add_forum_message(game, member, month, day, hour, minute, reset)
    # TODO(crem): Or what would be more appropriate response text?
    return HttpResponse('OK!')

  except tools.NotFound:
    raise Http404

  except tools.PermissionDenied:
    return HttpResponse(status=500)

