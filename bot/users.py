import django
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "snailbucket.settings"
django.setup()

import exceptions
import tournaments.models as db

def is_admin(who):
	admins = db.User.objects.filter(('username', who), ('is_superuser', True))
	return len(admins) == 1

def is_td(who):
	try:
		user_id = get_user_id_by_username(who)
	except exceptions.NoSuchUserError:
		return False
	# TODO: learn how to fetch tds
	print(dir(db))
	print(dir(db.models))
	print(dir(db.Bucket.tds))
	return len(db.Bucket.tds.filter(('member_id', user_id))) >= 1

def get_user_id_by_username(username):
	try:
		return db.User.objects.filter(('username', username))[0].id
	except:
		raise exceptions.NoSuchUserError(username)

# Below is for demo purpose only
if __name__ == '__main__':
	for user in ['PankracyRozumek', 'BethanyGrace', 'pchesso']:
		print('Is {} admin: {}\n'.format(user, is_admin(user)))
		print('Is {} td: {}\n'.format(user, is_td(user)))
