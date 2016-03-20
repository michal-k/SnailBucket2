from . import registration
from .models import Member
from django.test import TestCase

class RegistrationTest(TestCase):
  def test_successful_registration(self):
    # Create token.
    token = registration.GetRegistrationToken(
      'GMKramnik', 'kramnik@kramnik.com')
    # Check that token is valid.
    decoded_token = registration.CheckRegistrationToken(token)
    self.assertEqual(decoded_token,
      {'username': 'GMKramnik', 'email': 'kramnik@kramnik.com'})
    # Complete registration.
    registration.CompleteRegistration(token, 'password')
    # Check that user and member are created.
    self.assertTrue(Member.objects.filter(user__username='GMKramnik').exists())

