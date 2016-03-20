
from .models import Member
from django.contrib.auth.models import User
from django.core import signing
from django.core.mail import EmailMessage

class UserAlreadyExists(Exception):
  """Exception is thrown when user who wants to register already exists."""

def GetRegistrationToken(username, email):
  """Returns a user registration token.

  The registration token which should be sent to a user by email.
  It can should be passed back to CompleteRegistration function to complete
  registration.

  Arguments:
    username -- user name
    email -- user email
  Returns:
    Registration token, as a URL-safe string.
  Throws:
    UserAlreadyExists -- if user already completed registration.
  """
  if User.objects.filter(username=username).exists():
    raise UserAlreadyExists()
  return signing.dumps({'username': username, 'email': email},
                       salt='snail_reg', compress=True)


def CheckRegistrationToken(token):
  """Checks whether registation token is valid and decodes it.

  Argument:
    token -- registration token
  Returns:
    Object {username: <user name>, email: <user email>}
  Throws:
    django.core.signing.BadSignature -- if token is incorrect
    UserAlreadyExists -- if user is already registered
  """
  msg = signing.loads(token, salt='snail_reg')
  if User.objects.filter(username=msg['username']).exists():
    raise UserAlreadyExists()
  return msg


def CompleteRegistration(token, password):
  """Completes the registration of a user.

  Arguments:
    token -- registration token
    password -- password
    # country -- user's country
  Throws:
    django.core.signing.BadSignature -- if token is incorrect
    UserAlreadyExists -- if user is already registered
  """
  msg = CheckRegistrationToken(token)
  user = User.objects.create_user(msg['username'], msg['email'], password)
  user.save()
  member = Member.objects.create(user=user)
  member.save()


def SendActivationEmail(username, email):
  """Sends an activation email.

  Arguments:
    username -- user name
    email -- user email
  Throws:
    UserAlreadyExists -- if user already completed registration.
  """
  token = GetRegistrationToken(username, email)
  email = EmailMessage('Snailbucket account registration.',
    'Token is %s' % token, to=[email])
  email.send()

