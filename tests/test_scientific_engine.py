import unittest
from scientific_engine import simulate

class EngineTests(unittest.TestCase):
    def test_requires_consent(self):
        with self.assertRaises(PermissionError):
            simulate(["örnek"], "Durum", ["A", "B"])

    def test_requires_observations(self):
        with self.assertRaises(ValueError):
            simulate([], "Durum", ["A", "B"], consent=True)

    def test_requires_two_choices(self):
        with self.assertRaises(ValueError):
            simulate(["örnek"], "Durum", ["A"], consent=True)

if __name__ == "__main__":
    unittest.main()
