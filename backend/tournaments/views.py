from . import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json

def get_participants(request, tournament):
  buckets = get_object_or_404(models.Tournament, short_name=tournament
    ).bucket_set.all()

  res = [
    { 'name': b.name,
      'members': [ m.member.user.username for m in b.players.all() ]
    }
    for b in buckets
  ]

  return HttpResponse(json.dumps(res))