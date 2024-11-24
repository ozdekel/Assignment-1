import unittest

def gcd(a, b):
    if a == 0 and b == 0:
        return 0
    return abs(a) if b == 0 else gcd(b, a % b)

class TestGCD(unittest.TestCase):
    def test_gcd_positive_numbers(self):
        self.assertEqual(gcd(48, 18), 6)
        
    def test_gcd_negative_numbers(self):
        self.assertEqual(gcd(-48, -18), 6)

    def test_gcd_mixed_signs(self):
        self.assertEqual(gcd(-48, 18), 6)
        self.assertEqual(gcd(48, -18), 6)

    def test_gcd_with_zero(self):
        self.assertEqual(gcd(0, 5), 5)
        self.assertEqual(gcd(5, 0), 5)
        self.assertEqual(gcd(0, 0), 0)

    def test_gcd_prime_numbers(self):
        self.assertEqual(gcd(13, 17), 1)

    def test_gcd_same_number(self):
        self.assertEqual(gcd(7, 7), 7)

    def test_gcd_one(self):
        self.assertEqual(gcd(1, 5), 1)
        self.assertEqual(gcd(5, 1), 1)

    def test_gcd_large_numbers(self):
        self.assertEqual(gcd(123456, 789012), 12)

    def test_gcd_identity_property(self):
        self.assertEqual(gcd(0, 0), 0)
        self.assertEqual(gcd(10, 10), 10)

    def test_gcd_small_numbers(self):
        self.assertEqual(gcd(1, 1), 1)
        self.assertEqual(gcd(2, 1), 1)

if __name__ == '__main__':
    unittest.main()