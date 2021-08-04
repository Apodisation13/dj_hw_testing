from unittest import TestCase

from students.logic import func


class LogicTestCase(TestCase):
    def test_plus(self):
        result = func(2, 5, '+')
        self.assertEqual(result, 7)

    def test_minus(self):
        result = func(2, 5, '-')
        self.assertEqual(result, -3)

    def test_mul(self):
        result = func(2, 5, '+')
        self.assertEqual(result, 10)
