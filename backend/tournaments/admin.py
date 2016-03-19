from django.contrib import admin

from .models import *

class TournamentPlayerAdmin(admin.ModelAdmin):
  list_display = ('member', 'tournament_name', 'bucket_name')
  list_filter = ('bucket', 'member')
  def tournament_name(self, obj):
    return str(obj.bucket.tournament)
  def bucket_name(self, obj):
    return str(obj.bucket.name)

class RoundAdmin(admin.ModelAdmin):
  list_display = ('tournament', 'start')
  list_filter = ('tournament__name', 'start')


class RoundInline(admin.TabularInline):
    model = Round
    extra = 0

class TournamentAdmin(admin.ModelAdmin):
  list_display = ('name', 'short_name', 'signup_start', 'signup_end', 'rounds',
                  'is_active', 'games_left', 'last_played_game_date')
  list_filter = ('name', 'short_name', 'signup_start')
  inlines = [RoundInline, ]
  def rounds(self, obj):
    return str(obj.round_set.count())


class GameAdmin(admin.ModelAdmin):
  list_display = ('bucket', 'round', 'white_player', 'black_player', 'result')
  list_filter = ('bucket__tournament__name', 'bucket__name', 
                 'round', 'white_player', 'black_player', 'result')


class GameForumMessageAdmin(admin.ModelAdmin):
  list_display = ('game', 'member', 'time')
  list_filter = ('game__bucket__tournament__name',
                 'game__bucket__name',
                 ('member', admin.RelatedOnlyFieldListFilter), 'time')


class MemberAdmin(admin.ModelAdmin):
  list_display = ('name', 'reliability', 'suspended_until')


class BucketAdmin(admin.ModelAdmin):
  list_display = ('name', 'tournament')
  list_filter = ('name', 'tournament__name')


admin.site.register(Member, MemberAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Bucket, BucketAdmin)
admin.site.register(TournamentPlayer, TournamentPlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(GameForumMessage, GameForumMessageAdmin)
