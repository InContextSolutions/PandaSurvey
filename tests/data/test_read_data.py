import unittest
import PandasRake.datasets as datasets


def test_load_people():
    df = datasets.load_people()
    unittest.assertEqual(df.shape, (9999, 5))
