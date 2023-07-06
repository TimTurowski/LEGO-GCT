import unittest
from source.datastructures.einzelteil import Einzelteil

class MyTestCase(unittest.TestCase):
    def test_element_id_1(self):
        e1 = Einzelteil("6429054","FINAL BRICK 2X2")
        e1.element_id = "6429055"

        e2 = Einzelteil("6429055","FINAL BRICK 2X2")
        self.assertEqual(e1.element_id, e2.element_id)


if __name__ == '__main__':
    unittest.main()