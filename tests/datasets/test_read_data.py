import unittest
import PandaSurvey.datasets as datasets


class TestLoad(unittest.TestCase):

    def test_load_people(self):
        df = datasets.load_people()
        self.assertEqual(df.shape, (9999, 5))

    def test_load_sample_proportions(self):
        targets = datasets.load_sample_proportions()
        self.assertEqual(type(targets), type({}))
        self.assertEqual(len(targets), 5)
        self.assertEqual(len(targets['Age']), 5)

    def test_load_sample_weights(self):
        df = datasets.load_sample_weights()
        self.assertEqual(df.shape, (2092,))

    def test_load_sample_study(self):
        df = datasets.load_sample_study()
        self.assertEqual(df.shape, (2092, 6))
