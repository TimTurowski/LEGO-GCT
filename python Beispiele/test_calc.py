import unittest
import calc

class MyTestCase(unittest.TestCase):
    def test_add(self):
        self.assertEqual(calc.add(0, 1), 1)
        self.assertEqual(calc.add(4, 3), 7)
    def test_substract(self):
        self.assertEqual(calc.substract(4, 3), 1)
        self.assertEqual(calc.substract(0, 1), 1)

    def test_divide(self):
        self.ass
        self.assertEqual(calc.divide(4, 1), 4)
        self.assertRaises(ValueError, calc.divide, 1, 0)


if __name__ == '__main__':
    unittest.main()
