import unittest
from src.main import pozdrav

class TestMain(unittest.TestCase):
    def test_pozdrav(self):
        rezultat = pozdrav('Marijan')
        self.assertIn('Bok, Marijan', rezultat)

if __name__ == '__main__':
    unittest.main()
