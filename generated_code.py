"""
This module provides a function to compute the greatest common divisor (GCD)
of two integers and includes unit tests to verify its correctness.
"""

import unittest


def gcd(a, b):
    """
    Calculate the greatest common divisor (GCD) of two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The GCD of the two integers.
    """
    while b:
        a, b = b, a % b
    return abs(a)


class TestGCD(unittest.TestCase):
    """
    Unit test class for testing the gcd function.
    """

    def test_gcd_positive_numbers(self):
        """Test GCD with positive integers."""
        self.assertEqual(gcd(48, 18), 6)

    def test_gcd_with_one_zero(self):
        """Test GCD with one zero and one positive integer."""
        self.assertEqual(gcd(0, 5), 5)

    def test_gcd_with_both_zeros(self):
        """Test GCD with both integers as zero."""
        self.assertEqual(gcd(0, 0), 0)

    def test_gcd_negative_numbers(self):
        """Test GCD with negative integers."""
        self.assertEqual(gcd(-48, -18), 6)

    def test_gcd_with_negative_and_positive(self):
        """Test GCD with one negative and one positive integer."""
        self.assertEqual(gcd(-48, 18), 6)

    def test_gcd_of_primes(self):
        """Test GCD with two prime integers."""
        self.assertEqual(gcd(13, 17), 1)

    def test_gcd_one_large_and_one_small(self):
        """Test GCD with one large and one small integer."""
        self.assertEqual(gcd(1000000, 1000), 1000)

    def test_gcd_identical_numbers(self):
        """Test GCD with two identical integers."""
        self.assertEqual(gcd(42, 42), 42)

    def test_gcd_with_large_numbers(self):
        """Test GCD with two large integers."""
        self.assertEqual(gcd(123456, 789012), 12)

    def test_gcd_with_fractions_as_integers(self):
        """Test GCD with integers that are fractions."""
        self.assertEqual(gcd(2, 4), 2)


if __name__ == '__main__':
    unittest.main()
