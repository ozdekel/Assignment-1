"""This module implements the Euclidean algorithm to calculate the greatest common divisor (GCD)
of two integers and includes a suite of unit tests to verify its correctness."""

import unittest


def gcd(a, b):
    """Calculate the greatest common divisor (GCD) of two integers.

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
    """Unit tests for the gcd function."""

    def test_positive_numbers(self):
        """Test GCD for two positive numbers."""
        self.assertEqual(gcd(48, 18), 6)

    def test_same_number(self):
        """Test GCD when both numbers are the same."""
        self.assertEqual(gcd(42, 42), 42)

    def test_one_zero(self):
        """Test GCD when one number is zero."""
        self.assertEqual(gcd(0, 25), 25)
        self.assertEqual(gcd(25, 0), 25)

    def test_both_zero(self):
        """Test GCD when both numbers are zero."""
        self.assertEqual(gcd(0, 0), 0)

    def test_negative_numbers(self):
        """Test GCD for two negative numbers."""
        self.assertEqual(gcd(-48, -18), 6)
        self.assertEqual(gcd(-48, 18), 6)
        self.assertEqual(gcd(48, -18), 6)

    def test_prime_numbers(self):
        """Test GCD for two prime numbers."""
        self.assertEqual(gcd(13, 17), 1)

    def test_large_numbers(self):
        """Test GCD for large numbers."""
        self.assertEqual(gcd(270, 192), 6)

    def test_one_is_multiple_of_other(self):
        """Test GCD where one number is a multiple of the other."""
        self.assertEqual(gcd(15, 45), 15)

    def test_coprime_numbers(self):
        """Test GCD for two coprime numbers."""
        self.assertEqual(gcd(8, 15), 1)

    def test_euclidean_algorithm(self):
        """Test GCD using the Euclidean algorithm."""
        self.assertEqual(gcd(252, 105), 21)


if __name__ == '__main__':
    unittest.main()
