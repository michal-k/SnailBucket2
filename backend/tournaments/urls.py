from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^participants/(?P<tournament>\w+)$', views.get_participants)
]