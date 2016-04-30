from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^buckets/(?P<tournament>\w+)$', views.get_buckets),
  url(r'^game/(?P<game_id>\d+)/forum/addmessage$', views.add_forum_message),
  url(r'^pairings/(?P<tournament>\w+)/(?P<round>\d+)$', views.get_pairings),
  url(r'^participants/(?P<tournament>\w+)$', views.get_participants),
  url(r'^tournaments$', views.get_tournaments),  
]
