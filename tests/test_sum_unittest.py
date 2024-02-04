import unittest


class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 5, "Should be 5")
    
    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 6)), 9, "Should be 9")

if __name__ == '__main__':
    unittest.main()