# import unittest

# def factorize(x):
#     """ 
#     Factorize positive integer and return its factors.
#     :type x: int,>=0
#     :rtype: tuple[N],N>0
#     """
#     pass

class TestFactorize(unittest.TestCase):
    
    def test_wrong_types_raise_exception(self):
        for val in ['string', 1.5]:
            with self.subTest(val = val):
                self.assertRaises(TypeError, factorize, val)

    def test_negative(self):
        for val in [-1, -10, -100]:
            with self.subTest(val = val):
                self.assertRaises(ValueError, factorize, val)
    
    def test_zero_and_one_cases(self):
        for param, result in zip([0, 1], [(0,), (1,)]):
            with self.subTest(param = param, result = result):
                self.assertEqual(factorize(param), result)
    
    def test_simple_numbers(self):
        params = [3, 13, 29]
        results = [(3,), (13,), (29,)]
        for param, result in zip(params, results):
            with self.subTest(param = param, result = result):
                self.assertEqual(factorize(param), result)
    
    def test_two_simple_multipliers(self):
        params = [6, 26, 121]
        results = [(2, 3), (2, 13), (11, 11)]
        for param, result in zip(params, results):
            with self.subTest(param = param, result = result):
                self.assertEqual(factorize(param), result)
    
    def test_many_multipliers(self):
        params = [1001, 9699690]
        results = [(7, 11, 13), (2, 3, 5, 7, 11, 13, 17, 19)]
        for param, result in zip(params, results):
            with self.subTest(param = param, result = result):
                self.assertEqual(factorize(param), result)