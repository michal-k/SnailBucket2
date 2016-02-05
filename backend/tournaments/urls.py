from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^participants/(?P<tournament>\w+)$', views.get_participants),
  url(r'^game/(?P<game_id>\d+)/forum/addmessage$', views.add_forum_message),
]