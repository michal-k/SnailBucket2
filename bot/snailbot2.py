import django
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "snailbucket.settings"
django.setup()

import telnetlib
import re
import sys

import pending
import tournaments.models as db
import users

host = 'www.freechess.org'

users_not_to_answer = ['roboadmin']

def bt(s):
	return s.encode(encoding='UTF-8')

def login(conn):
	lines = conn.read_until(b'login: ').split(b'\n')
	for line in lines:
		print(line)
	conn.write(b'snailbotdev\n')
	conn.write(b'\n')

def init(conn):
	conn.write(b'set seek 0\n')
	conn.write(b'-ch 53\n')

def tell(who, what):
	conn.write(bt('tell {} {}\n'.format(who, what)))

def qtell(who, what):
	conn.write(bt('qtell {} {}\n'.format(who, what)))

def observe(who, what):
	m = re.search('observe ([^ ]*)', what)
	if m:
		# TODO: check if this is a snailbot game before actually observing.
		tell(who, 'Starting to follow {}'.format(m.group(1)))
		conn.write(bt('observe {}\n'.format(m.group(1))))
		conn.write(bt('+gnotify {}\n'.format(m.group(1))))
		return
	tell(who, 'Wrong syntax of observe command')
		

def handle_tell(who, what):
	who = who.lstrip()
	for user in users_not_to_answer:
		if re.search(user, who, flags=re.IGNORECASE):
			print('Ignoring user {}'.format(who))
			return
	
	what = what.lstrip()
	if re.search('^play$', what, flags=re.IGNORECASE):
		tell(who, 'Not implemented')
		# TODO: call function starting the game here.
	elif re.search('^ngames', what, flags=re.IGNORECASE):
		qtell(who, 'Pending games:\n{}'.format(pending.get_pending_as_string()))
	elif re.search('^observe', what, flags=re.IGNORECASE):
		if users.is_admin(who) or users.is_td(who):
			# Ask the bot to observe particular game.
			observe(who, what)
		else:
			tell(who, 'Command unknown: {}'.format(what))
	else:
		tell(who, 'Command unknown: {}'.format(what))


conn = telnetlib.Telnet(host)
login(conn)
init(conn)
line = conn.read_until(b'\n').decode(encoding='UTF-8')
while line:
	print(line.strip())
	m = re.search('(.*) tells you: (.*)', line)
	if m:
		handle_tell(m.group(1), m.group(2))
	m = re.search('{Game [0-9]* \(([^ ]*) vs. ([^ ]*)\) .*} ([^ ]*)', line)
	if m:
		print('Reported game: {}-{} {}'.format(m.group(1), m.group(2), m.group(3)))
		# TODO: call function reporting game result here.
		# -gnotify both players here.
		
	line = conn.read_until(b'\n').decode(encoding='UTF-8')
	

	
