from django.test import TestCase
from . import tools

class Tournament:
  def __init__(self, min_size, max_size, rounds, type_code):
    self.bucketgen_min_bucket_size = min_size
    self.bucketgen_max_bucket_size = max_size
    self.roundsgen_round_count = rounds
    self.type_code = type_code

class ToolsTestCase(TestCase):

  def test_generate_bucket_sizes_swiss(self):
    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(0, 0, rounds=5, type_code='Swiss'), 96),
        [32, 32, 32])

    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(0, 0, rounds=5, type_code='Swiss'), 95),
        [32, 32, 31])

    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(0, 0, rounds=5, type_code='Swiss'), 94),
        [32, 32, 30])

    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(0, 0, rounds=5, type_code='Swiss'), 93),
        [32, 30, 31])

    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(0, 0, rounds=5, type_code='Swiss'), 92),
        [32, 30, 30])

    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(0, 0, rounds=5, type_code='Swiss'), 91),
        [31, 30, 30])

    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(0, 0, rounds=5, type_code='Swiss'), 97),
        [25, 24, 24, 24])

  def test_generate_bucket_sizes_rr(self):
    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(7, 8, rounds=None, type_code='RR'), 48),
        [8, 8, 8, 8, 8, 8])
   
    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(7, 8, rounds=None, type_code='RR'), 47),
        [8, 8, 8, 8, 8, 7])
   
    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(7, 8, rounds=None, type_code='RR'), 46),
        [7, 8, 8, 8, 8, 7])
   
    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(7, 8, rounds=None, type_code='RR'), 45),
        [7, 7, 8, 8, 8, 7])
   
    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(7, 8, rounds=None, type_code='RR'), 43),
        [7, 7, 7, 7, 8, 7])
   
    self.assertEquals(
        tools.generate_bucket_sizes(Tournament(7, 8, rounds=None, type_code='RR'), 42),
        [7, 7, 7, 7, 7, 7])

    with self.assertRaises(tools.InvalidParameters):
      tools.generate_bucket_sizes(Tournament(7, 8, rounds=None, type_code='RR'), 41)
