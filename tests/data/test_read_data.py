import unittest
import pandasurvey.datasets as datasets


class TestLoad(unittest.TestCase):

    def test_load_people(self):
        df = datasets.load_people()
        self.assertEqual(df.shape, (9999, 6))

    def test_load_target_weights(self):
        targets = datasets.load_target_weights()
        self.assertEqual(type(targets), type({}))

    def test_load_rengine_weights(self):
        df = datasets.load_rengine_weights()
        self.assertEqual(df.shape, (2094, 20))
