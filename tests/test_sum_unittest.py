import unittest


class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple_1(self):
        self.assertEqual(sum((1, 2, 2)), 5, "Should be 5")
    
    def test_sum_tuple_2(self):
        self.assertEqual(sum((1, 2, 6)), 9, "Should be 9")

    def test_sum_tuple_3(self):
        self.assertEqual(sum((1, 2, 7)), 10, "Should be 10")

    def test_sum_prod(self):
        self.assertEqual(3*3, 9, "Should be 9")

if __name__ == '__main__':
    unittest.main()