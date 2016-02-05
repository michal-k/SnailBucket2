import django
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "snailbucket.settings"
django.setup()

import tournaments.models as db
import users

def get_pending():
	games = []
	for game in (db.Game.objects.filter(('scheduled_time__isnull', 0), ('result', '?-?'))
			.order_by('scheduled_time').values()):
		games.append(expand_foreign_keys_names(game))
	return games

def get_pending_for_player(username):
	user_id = users.get_user_id_by_username(username)

	games = []
	for game in db.Game.objects.filter(
			('scheduled_time__isnull', 0), ('white_player_id', user_id), ('result', '?-?')).values():
		games.append(expand_foreign_keys_names(game))
	for game in db.Game.objects.filter(
			('scheduled_time__isnull', 0), ('black_player_id', user_id), ('result', '?-?')).values():
		games.append(expand_foreign_keys_names(game))
		
	return games

def expand_foreign_keys_names(game):
	game['white_player'] = db.User.objects.filter(('id', game['white_player_id']))[0].username
	game['black_player'] = db.User.objects.filter(('id', game['black_player_id']))[0].username
	bucket = db.Bucket.objects.filter(('id', game['bucket_id']))[0]
	game['bucket'] = bucket.name
	game['tournament'] = db.Tournament.objects.filter(('id', bucket.tournament_id))[0].name
	return game

def get_pending_as_string():
	games = get_pending()
	output = 'Tournament            | Bucket | Round | White | Black | Time\n'
	for game in games:
		output += '{} | {} | {} | {} | {} | {}\n'.format(
			game['tournament'],
			game['bucket'],
			game['round'],
			game['white_player'],
			game['black_player'],
			game['scheduled_time'])
	return output



# The following is for demo purpose only.
if __name__ == "__main__":
	print('All pending games are:')
	for game in get_pending():
		print(game)
	print()

	print(get_pending_as_string())
	print()

	for player in ['pchesso', 'PankracyRozumek', 'BethanyGrace', 'nonexistingplayer']:
		print('All pending games of {} are:'.format(player))
		try:
			games = get_pending_for_player(player)
			if len(games):
				for game in games:
					print(game)
			else:
				print('No games for player {}'.format(player))
		except:
			print('No such user')
		print()

