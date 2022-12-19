"""
sample test
"""
from django.test import SimpleTestCase

from .calc import *

class CalcTest(SimpleTestCase):
    """test the calc module"""

    def test_add_number(self):
        res = calc(5, 6)

        self.assertEqual(res, 11)

    def test_subtract_number(self):
        res = subtract(10, 15)

        self.assertEqual(res, 3)