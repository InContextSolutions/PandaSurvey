import unittest
import PandasRake.datasets as datasets


class TestLoad(unittest.TestCase):

    def test_load_people(self):
        df = datasets.load_people()
        self.assertEqual(df.shape, (9999, 6))
