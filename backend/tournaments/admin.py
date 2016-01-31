from django.contrib import admin

from .models import *

class TournamentPlayerAdmin(admin.ModelAdmin):
  list_display = ('tournament', 'member')


class BucketPlayerAdmin(admin.ModelAdmin):
  list_display = ('tournament_name', 'bucket_name', 'member')
  def tournament_name(self, obj):
    return str(obj.bucket.tournament)
  def bucket_name(self, obj):
    return str(obj.bucket.name)


admin.site.register(Member)
admin.site.register(Tournament)
admin.site.register(Round)
admin.site.register(Bucket)
admin.site.register(BucketPlayer, BucketPlayerAdmin)
admin.site.register(TournamentPlayer, TournamentPlayerAdmin)
admin.site.register(Game)
admin.site.register(GameForumMessage)
