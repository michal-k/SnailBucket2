class NoSuchUserError(BaseException):
	def __init__(self, username):
		self.username = username

	def __str__(self):
		return self.username
