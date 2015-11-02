from django.contrib import admin

from .models import *

admin.site.register(Member)
admin.site.register(Tournament)
admin.site.register(Round)
admin.site.register(Bucket)
admin.site.register(BucketPlayer)
admin.site.register(TournamentPlayer)
admin.site.register(Game)
admin.site.register(GameForumMessage)
